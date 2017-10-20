from src.resources import load_resource
from src.context import value_from_key_lookup


class ApplicationInterface:
    def __init__(self, class_dict, environment, interface_name):
        self.class_dict = class_dict
        self.environment = environment
        self.interface_name = interface_name

    def apply_interface(self):
        cfg = load_resource(self.environment.name)
        ci = cfg[self.interface_name]

        for name in ci:
            entity = self.environment.model[name]
            entry = ci[name]

            for method_name in entry:
                args = entry[method_name]
                if type(args) is not list:
                    args = [args]

                self.handle_entity(method_name, entity, *args)

    def handle_entity(self, method_name, entity, *args):
        pass

    def get_value_from_model(self, value):
        return value_from_key_lookup(
            value, self.class_dict, self.environment.model
        )

    def get_interface_method(self, method_name, entity, *args):
        args = self.get_value_from_model(args)
        m = getattr(self, method_name)

        def interface_method():
            m(
                entity, *args
            )

        return interface_method
