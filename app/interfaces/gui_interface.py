from src.context import ApplicationInterface
from app.sprites.hud_sprite import HudSprite
from os import listdir
from os.path import join


class GuiInterface(ApplicationInterface):
    INTERFACE_NAME = "gui interface"

    def __init__(self, context, environment):
        super(GuiInterface, self).__init__(
            context, environment, GuiInterface.INTERFACE_NAME
        )

    def get_menu_from_entity(self, block, entity):
        self.set_menu(block, entity.get_menu())

    def get_menu_from_directory(self, block, *path):
        path = join(*path)
        files = listdir(path)

        names = (self.environment.name, self.environment.name + ".cfg")
        file_names = [f for f in files if f not in names]

        table = []
        for file_name in file_names:
            row = [
                {
                    "name": "Load {}".format(file_name),
                    "on_activate": ["transition_to", "environment", file_name]
                }
            ]
            table.append(row)

        self.set_menu(block, table)

    def add_return_option(self, block):
        option = self.get_option(
            block, {
                "name": "Return Option",
                "text": "Exit",
                "on_activate": ["handle_event", block, "return"]
            }
        )

        new_table = [[option]]
        block.add_members(new_table)
        block.add_listener({
            "name": "return",
            "target": self.environment,
            "response": "return"
        })

    def get_option(self, block, d):
        name = d.pop("name")
        option = HudSprite(name)

        selectable = True
        if "selectable" in d:
            selectable = d.pop("selectable")

        if not selectable:
            option.on_select = False

        if "on_activate" in d:
            args = self.get_value_from_model(
                d.pop("on_activate")
            )
            self.set_activate_method(
                option, *args
            )

        if "listeners" in d:
            listeners = d.pop("listeners")
            for l in listeners:
                if "target" in l:
                    if l["target"] == "menu":
                        l["target"] = block

            option.add_listener(*listeners)

        self.context.init_item(
            self.environment.model, option, d
        )

        return option

    def set_menu(self, block, table):
        new_table = []
        for row in table:

            new_row = []
            for item in row:

                if item:
                    new_row.append(
                        self.get_option(
                            block, item
                        )
                    )
                else:
                    new_row.append(None)

            new_table.append(new_row)

        block.set_members(new_table)

    def set_activate_method(self, option, method_name, target, *args):
        m = None
        if hasattr(self, method_name):
            m = getattr(self, method_name)
        elif hasattr(target, method_name):
            m = getattr(target, method_name)

        if callable(m):
            def on_activate():
                m(*args)

            option.on_activate = on_activate
        elif m is not None:
            raise ValueError("{} is not callable".format(m))


