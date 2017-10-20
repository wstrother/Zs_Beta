from app.interface import ApplicationInterface


class ControllerInterface(ApplicationInterface):
    INTERFACE_NAME = "controller interface"
    DPAD = "Dpad"

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
    def move_pointer(sprite):
        dpad = sprite.controller.get_device(
            ControllerInterface.DPAD
        )

        if dpad.check():
            dx, dy = dpad.get_direction()
            sprite.move_pointer(dx, dy)

    @staticmethod
    def move(sprite, speed):
        dpad = sprite.controller.get_device(
            ControllerInterface.DPAD
        )

        if dpad.held:
            dx, dy = dpad.get_direction()
            sprite.move(dx, dy, speed)

    @staticmethod
    def cycle_animation(sprite, button):
        b = sprite.controller.get_device(
            button
        )

        if b.check():
            names = sprite.get_animation_states()
            current = sprite.animation_state
            i = names.index(current)
            i += 1
            i %= len(names)
            sprite.set_animation_state(names[i])
