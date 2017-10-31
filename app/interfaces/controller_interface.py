from src.context import ApplicationInterface


class ControllerInterface(ApplicationInterface):
    INTERFACE_NAME = "controller interface"
    DPAD = "Dpad"
    ACTIVATION = "A", "Start"

    def __init__(self, class_dict, environment):
        super(ControllerInterface, self).__init__(
            class_dict, environment,
            ControllerInterface.INTERFACE_NAME
        )

    def handle_entity(self, method_name, entity, *args):
        entity.update_methods.append(
            self.get_interface_method(
                method_name, entity, *args
            )
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

        if any([b.check() for b in buttons]):
            block.members.active_member.handle_event("activate")

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
            sprite.handle_event(movement)

    @staticmethod
    def cycle_animation(sprite, button):
        b = sprite.controller.get_device(
            button
        )

        if b.check():
            sprite.handle_event('cycle_animation')
