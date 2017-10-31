from zs_globals import Cfg
from src.collections import Group
from src.resources import load_resource
from src.entities import Environment, Layer, Sprite

# ===================================
# DEFINE THE DEFAULT CLASS DICTIONARY
# ===================================

CLASS_DICT = {
        "Layer": Layer,
        "Environment": Environment,
        "Sprite": Sprite
    }


class Context:
    def __init__(self, class_dict, *interfaces):
        self.class_dict = CLASS_DICT
        if class_dict:
            self.class_dict.update(class_dict)

        self.interfaces = interfaces

    def get_environment(self, name):
        env = Environment(name)
        cfg = load_resource(name)

        self.set_environment_context(cfg, env)

        return env

    def apply_interfaces(self, env):
        for interface in self.interfaces:
            interface(self, env).apply_interface(
                load_resource(
                    env.name, section=interface.INTERFACE_NAME
                )
            )

    def set_environment_context(self, cfg, env, p=False):
        self.update_model(cfg, env)
        self.add_layers(cfg, env, p=p)
        self.populate(cfg, env, p=p)

    def get_spawn_method(self, cls):
        """
        returns callable method for entity objects
          from imported modules in class_dict
        """
        def spawn(name):
            return self.class_dict[cls](name)

        return spawn

    def update_model(self, cfg, environment, p=False):
        """
        updates environment model {} object based
              on imported class_dict and cfg data
        """
        model = environment.model
        model["environment"] = environment

        if p:
            print("\nUpdating Model for {}".format(environment))

        for section in cfg:
            current = cfg[section]

            for name in current:
                entry = current[name]

                if section == Cfg.GROUPS:
                    item = Group(name)

                elif section in Cfg.CONSTRUCTOR_SECTIONS:
                    item = self.get_spawn_method(
                        entry[Cfg.CLASS_KEYWORD]
                        )(name)

                else:
                    item = self.value_from_key_lookup(
                        name, model
                    )

                if section != Cfg.POPULATE:
                    if p:
                        print("\t{} added to model".format(name))
                    model[name] = item

    def add_layers(self, log_cfg, environment, p=False):
        """
        adds layers specified in cfg section to
          an environment object
        """
        layers = log_cfg[Cfg.LAYERS]
        model = environment.model

        for name in layers:
            #                       # Add / initialize layer objects for environment
            item_cfg = layers[name]
            layer = model[name]

            if Cfg.PARENT_LAYER not in item_cfg:
                parent = environment
                log_cfg = False

            else:
                parent = model[item_cfg[Cfg.PARENT_LAYER]]
                log_cfg = True

            layer.set_parent_layer(parent, log_cfg)

            self.init_item(
                model, layer, item_cfg, p=p
            )

    def populate(self, cfg, environment, p=False):
        """
        populates an Environment object with sprite objects
            and adds them to designated groups
        """
        model = environment.model
        pd = cfg[Cfg.POPULATE]

        for name in pd:
            # Add / initialize sprite objects for environment
            item_cfg = pd[name]

            spawn = self.get_spawn_method(item_cfg[Cfg.CLASS_KEYWORD])

            item = spawn(name)

            self.init_item(
                model, item, item_cfg, p=p
            )

            if Cfg.ADD_TO_MODEL in item_cfg:
                model[item.name] = item
                item.cfg_dict[Cfg.ADD_TO_MODEL] = True

    def init_item(self, model, item, item_cfg, p=False):
        """
        automatically looks up and calls interface methods
            corresponding to the item_cfg data parameters
        """
        keys = [k for k in item_cfg]
        order = item.init_order

        if p:
            print("\nInitializing {}".format(item))

        # setter methods not listen in 'init_order' will
        # be called afterwards
        if order:
            attrs = [
                o for o in order if o in keys
                ] + [
                k for k in keys if k not in order
            ]

        else:
            attrs = keys

        # call set_attribute methods on item for values in dict
        for attr in attrs:
            set_attr = "set_" + attr

            if hasattr(item, set_attr):
                if p:
                    print("\t{}".format(set_attr))

                # match value keys from class_dict and model
                value = self.value_from_key_lookup(
                    item_cfg[attr], model)

                # call the setter method with args
                if type(value) is list:
                    args = value
                else:
                    args = [value]
                getattr(item, set_attr)(*args)

                if p:
                    print("\targs: {}\n".format(args))

            elif attr not in Cfg.INIT_KEYS:
                msg = "no {} method for {}".format(
                    set_attr, item)

                print(msg)

    def value_from_key_lookup(self, value, model):
        """
        looks up corresponding keys to data argument in
          the imported class_dict and data model
        """
        def get(k, m):
            if k == Cfg.MODEL:
                return m

            if k in self.class_dict:
                return self.class_dict[k]

            if k in m:
                return m[k]

            else:
                return k

        if type(value) is list:
            new = []
            for item in value:
                new.append(
                    get(item, model)
                )

            return new

        elif type(value) is dict:
            for key in value:
                if value[key] is True:
                    value[key] = get(key, model)

            return value

        else:
            return get(value, model)


class ApplicationInterface:
    def __init__(self, context, env, name):
        self.context = context
        self.interface_name = name
        self.environment = env

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
        self.get_interface_method(
            method_name, entity, *args
        )()

    def get_value_from_model(self, value):
        if type(value) is tuple:
            value = list(value)

        return self.context.value_from_key_lookup(
            value, self.environment.model
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
