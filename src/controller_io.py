from src.controller import Button, Dpad, Controller, Trigger, ThumbStick
from src.input_manager import ButtonMappingKey, ButtonMappingButton, ButtonMappingAxis, ButtonMappingHat, AxisMapping
from src.resources import load_resource
from zs_globals import ControllerInputs as ConIn


class ControllerIO:
    #
    # USB device / Keyboard mapping and input manager
    #
    #
    # methods for loading a controller object from a cfg formatted text stream
    # or json formatted dictionary
    #

    DEVICES_DICT = {
        "button": Button,
        "dpad": Dpad,
        "trigger": Trigger,
        "thumb_stick": ThumbStick,
        "button_map_key": ButtonMappingKey,
        "button_map_button": ButtonMappingButton,
        "button_map_axis": ButtonMappingAxis,
        "button_map_hat": ButtonMappingHat,
        "axis_map": AxisMapping,
    }

    # return a controller object from a cfg formatted file
    @staticmethod
    def load_controller(file_name):
        devices = load_resource(file_name + ".cfg")["devices"]

        return ControllerIO.make_controller(
            file_name, devices)

    # return a controller object from a json formatted devices dict
    @staticmethod
    def make_controller(name, devices):
        # print_dict(devices)
        controller = Controller(name)

        try:
            for name in devices:
                d = devices[name]
                cls = ControllerIO.get_device_class(d)

                mapping = ControllerIO.get_mapping(d)
                device = cls(name)

                controller.add_device(
                    device, mapping
                )

            return controller

        except IndexError:
            raise IOError("Unable to build controller " + name)
        except AssertionError:
            raise IOError("Unable to build controller " + name)

    @staticmethod
    def get_device_class(d):
        return ControllerIO.DEVICES_DICT[d["class"]]

    @staticmethod
    def get_mapping(d):
        def get_m(md):
            c = md[0]
            a = md[1:]

            return ControllerIO.DEVICES_DICT[c](*a)

        if d["class"] in ("button", "trigger"):
            return get_m(d["mapping"])

        if d["class"] == "dpad":
            return [
                get_m(d[direction]) for direction in ConIn.UDLR
            ]

        if d["class"] == "thumb_stick":
            return [
                get_m(d[axis]) for axis in ConIn.AXES
            ]
