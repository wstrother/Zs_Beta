from app.interface import ApplicationInterface


class ControllerInterface(ApplicationInterface):
    DPAD = "Dpad"

    def __init__(self, class_dict, environment):
        super(ControllerInterface, self).__init__(
            class_dict, environment, "controller interface"
        )

    def get_interface_method(self, method_name, entity, *args):
        args = self.get_value_from_model(list(args))
        layer = args.pop(0)
        args[0] = layer.controllers[args[0]]

        return super(ControllerInterface, self).get_interface_method(
            method_name, entity, *args
        )

    def handle_entity(self, method_name, entity, *args):
        entity.update_methods.append(
            self.get_interface_method(
                method_name, entity, *args
            )
        )

    @staticmethod
    def move(sprite, controller, speed):
        dpad = controller.get_device(ControllerInterface.DPAD)

        if dpad.held:
            dx, dy = dpad.get_direction()
            sprite.move(dx, dy, speed)

    @staticmethod
    def cycle_animation(sprite, controller, button):
        b = controller.get_device(button)

        if b.check():
            names = sprite.get_animation_states()
            current = sprite.animation_state
            i = names.index(current)
            i += 1
            i %= len(names)
            sprite.set_animation_state(names[i])
