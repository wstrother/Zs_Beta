from app.interface import ApplicationInterface


class GuiInterface(ApplicationInterface):
    def __init__(self, class_dict, environment):
        super(GuiInterface, self).__init__(
            class_dict, environment, "gui interface"
        )

    def handle_entity(self, method_name, entity, *args):
        self.get_interface_method(
            method_name, entity, *args
        )()
