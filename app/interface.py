from src.resources import load_resource
from src.context import value_from_key_lookup


class ApplicationInterface:
    def __init__(self, class_dict, environment, name):
        self.class_dict = class_dict
        self.environment = environment
        self.interface_name = name

    def apply_interface(self, d):
        for name in d:
            entity = self.environment.model[name]
            entry = d[name]

            for method_name in entry:
                args = entry[method_name]
                if type(args) is not list:
                    args = [args]

                self.handle_entity(method_name, entity, *args)

    def handle_entity(self, method_name, entity, *args):
        pass

    def get_value_from_model(self, value):
        if type(value) is tuple:
            value = list(value)

        return value_from_key_lookup(
            value, self.class_dict, self.environment.model
        )

    def get_interface_method(self, method_name, entity, *args):
        if args == (True,):
            args = []

        args = self.get_value_from_model(args)
        m = getattr(self, method_name)

        def interface_method():
            m(
                entity, *args
            )

        return interface_method
