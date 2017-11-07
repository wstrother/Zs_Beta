from src.context import ApplicationInterface
from app.sprites.hud_sprite import HudSprite
from os import listdir
from os.path import join


class GuiInterface(ApplicationInterface):
    def __init__(self, context):
        name = "gui_interface"
        super(GuiInterface, self).__init__(context, name)

        self.init_order = [
            "get_menu_from_entity",
            "get_menu_from_directory",
            "add_return_option"
        ]

    def handle_data_item(self, entity, method_name, *args):
        if args == (True, ):
            args = ()

        self.call_method_on_entity(
            entity, method_name, *args
        )

    def get_menu_from_directory(self, block, *path):
        path = join(*path)
        print(path)
        files = listdir(path)
        environment = self.context.model["environment"]

        names = (environment.name, environment.name + ".cfg")
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

    def get_menu_from_entity(self, block, entity):
        print("\t\t!!!{}".format(entity))
        self.set_menu(block, entity.get_menu())

    def get_pause_menu(self, layer):
        data = layer.get_pause_menu_data()

        block = self.context.add_entity(
            "Pause Menu Block", data, model=False
        )
        self.context.set_attributes(block, data)
        self.context.apply_interfaces(block, data)

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

    def get_option(self, block, d):
        name = d.pop("name")
        option = HudSprite(name)

        selectable = True
        if "selectable" in d:
            selectable = d.pop("selectable")

        if not selectable:
            option.on_select = False

        if "on_activate" in d:
            args = self.context.get_value(
                d.pop("on_activate")
            )

            if args[1] == "block":
                args[1] = self

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

        self.context.set_attributes(
            option, d
        )

        return option

    @staticmethod
    def set_activate_method(option, method_name, target, *args):
        m = None

        if hasattr(target, method_name):
            m = getattr(target, method_name)

        if callable(m):
            def on_activate():
                m(*args)

            option.on_activate = on_activate

        elif m is not None:
            raise ValueError("{} is not callable".format(m))

    def add_return_option(self, block, text):
        option = self.get_option(
            block, {
                "name": "Return Option",
                "text": text,
                "on_activate": ["handle_event", block, "return"]
            }
        )

        environment = self.context.model["environment"]
        new_table = [[option]]
        block.add_members(new_table)
        block.add_listener({
            "name": "return",
            "target": environment,
            "response": "return"
        })
