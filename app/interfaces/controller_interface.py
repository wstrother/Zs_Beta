from src.context import ApplicationInterface


class ControllerInterface(ApplicationInterface):
    DPAD = "Dpad"
    ACTIVATION = ("A",)

    def __init__(self, context):
        name = "controller_interface"
        super(ControllerInterface, self).__init__(
            context, name
        )

    def handle_data_item(self, entity, method_name, *args):
        if args == (True,):
            args = ()

        self.add_update_method(
            entity, method_name, entity, *args
        )

    @staticmethod
    def move_pointer(block):
        dpad = block.controller.get_device(
            ControllerInterface.DPAD
        )

        if dpad.check():
            dx, dy = dpad.get_direction()
            movement = {
                'name': 'move_pointer',
                'value': [dx, dy]
            }
            block.handle_event(movement)

    @staticmethod
    def check_activation(block):
        buttons = [
            block.controller.get_device(n) for n in ControllerInterface.ACTIVATION
            ]

        if block.members.active_member and any([b.check() for b in buttons]):
                block.members.active_member.queue_event("activate")

    @staticmethod
    def check_pause_layer(layer, pause_layer):
        if layer.controllers:
            controller = layer.controllers[0]
            b = controller.get_device("Start")

            if b.check():
                print("PAUSE LAYER")
                pause_layer.handle_event("pause")

    @staticmethod
    def move(sprite, speed):
        dpad = sprite.controller.get_device(
            ControllerInterface.DPAD
        )

        if dpad.held:
            dx, dy = dpad.get_direction()

            movement = {
                'name': 'move',
                'value': [dx, dy],
                'speed': speed
            }

            sprite.queue_event(movement)

    @staticmethod
    def cycle_animation(sprite, button):
        b = sprite.controller.get_device(
            button
        )

        if b.check():
            sprite.queue_event('cycle_animation')
