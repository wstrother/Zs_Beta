from app.interface import ApplicationInterface
from app.sprites.hud_sprite import HudSprite
from src.context import init_item


class GuiInterface(ApplicationInterface):
    INTERFACE_NAME = "gui interface"

    def __init__(self, class_dict, environment):
        super(GuiInterface, self).__init__(
            class_dict, environment, GuiInterface.INTERFACE_NAME
        )

    def handle_entity(self, method_name, entity, *args):
        if not hasattr(self, method_name):
            i = int(method_name)
            method_name = "set_option"
            option = entity.get_option(i)
            entity = option

        self.get_interface_method(
            method_name, entity, *args
        )()

    def get_menu_from_entity(self, block, entity):
        new_table = []
        for row in entity.get_menu():
            new_row = []
            for item in row:
                if item:
                    new_row.append(self.get_option(
                        block, entity, item
                    ))
                else:
                    new_row.append(None)
            new_table.append(new_row)

        block.set_members(new_table)
        block.set_group(self.get_value_from_model(block.group))
        block.set_table_positions()

    def get_option(self, block, entity, d):
        name = d.pop("name")
        option = HudSprite(name)

        selectable = True
        if "selectable" in d:
            selectable = d.pop("selectable")

        if not selectable:
            option.on_select = False

        if "on_activate" in d:
            args = d.pop("on_activate")
            self.set_activate_method(
                entity, option, *args
            )

        if "listeners" in d:
            listeners = d.pop("listeners")
            for l in listeners:
                if "target" in l:
                    if l["target"] == "menu":
                        l["target"] = block

            option.add_listener(*listeners)

        init_item(
            self.class_dict, self.environment.model,
            option, d
        )

        return option

    def set_activate_method(self, entity, option, method_name, *args):
        m = None
        if hasattr(self, method_name):
            m = getattr(self, method_name)
        elif hasattr(entity, method_name):
            m = getattr(entity, method_name)

        if callable(m):
            def on_activate():
                m(*args)

            option.on_activate = on_activate
        elif m is not None:
            raise ValueError("{} is not callable".format(m))

    @staticmethod
    def cycle_animation(sprite):
        names = sprite.get_animation_states()
        current = sprite.animation_state
        i = names.index(current)
        i += 1
        i %= len(names)
        sprite.set_animation_state(names[i])

