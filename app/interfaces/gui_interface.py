from app.interface import ApplicationInterface


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

    def get_menu_from_entity(self, block, entity, menu):
        table = [[]]
        if menu == "animation":
            table = self.animation_sprite_menu(entity)
        block.set_members(table)
        block.set_group(self.get_value_from_model(block.group))

    def set_option(self, option, method_name, *args):
        m = getattr(self, method_name, None)
        if callable(m):
            def on_activate():
                m(*args)

            option.on_activate = on_activate
        else:
            raise ValueError("{} is not callable".format(m))

    @staticmethod
    def animation_sprite_menu(entity):
        return {
            0: [entity.name],
            1: [entity.size],
            2: [entity.position],
            3: ["Change Animation"]
        }

    @staticmethod
    def cycle_animation(sprite):
        names = sprite.get_animation_states()
        current = sprite.animation_state
        i = names.index(current)
        i += 1
        i %= len(names)
        sprite.set_animation_state(names[i])
