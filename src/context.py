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


class NewContext:
    def __init__(self, class_dict, *interfaces):
        self.class_dict = CLASS_DICT
        if class_dict:
            self.class_dict.update(class_dict)

        self.interfaces = interfaces
        self.model = {}

    def get_environment(self, name):
        env = Environment(name)
        cfg = load_resource(name)

        self.set_environment_context(cfg, env)

        return env

    def get_spawn_method(self, cls):
        """
        returns callable method for entity objects
          from imported modules in class_dict
        """

        def spawn(name):
            return self.class_dict[cls](name)

        return spawn

    @staticmethod
    def log_item(item, name=None):
        if not name:
            name = item.name

        print("{} created and added to model[{}]".format(
            item, name
        ))

    def get_value(self, value):
        """
        looks up corresponding keys to data argument in
          the imported class_dict and data model
        """
        def get(k):
            if k == Cfg.MODEL:
                return self.model

            if k in self.class_dict:
                return self.class_dict[k]

            if k in self.model:
                return self.model[k]

            else:
                return k

        if type(value) is list:
            new = []
            for item in value:
                new.append(get(item))

            return new

        elif type(value) is dict:
            for key in value:
                if value[key] is True:
                    value[key] = get(key)

            return value

        else:
            return get(value)

    def set_environment_context(self, cfg, env, p=False):
        self.model["environment"] = env

        groups = cfg.pop("groups")
        self.add_groups(groups, p=p)

        layers = cfg.pop("layers")
        self.add_entities(layers, layer=True, p=p)

        sprites = cfg.pop("sprites")
        self.add_entities(sprites, p=p)

        for section in cfg:
            self.update_model(section, p=False)

    def update_model(self, section, p=False):
        for name in section:
            item = self.get_value(name)
            self.model[name] = item

            if p:
                self.log_item(item, name=name)

    def add_groups(self, section, p=False):
        for group_name in section:
            group = Group(group_name)
            self.model[group_name] = group

            if p:
                self.log_item(group)

    def add_entities(self, section, layer=False, p=False):
        for item_name in section:
            data = section[item_name]

            item = self.get_spawn_method(
                data[Cfg.CLASS_KEYWORD]
            )(item_name)
            self.model[item_name] = item

            if layer:
                if Cfg.PARENT_LAYER not in data:
                    parent = self.model["environment"]
                    log_cfg = False

                else:
                    parent = self.model[data[Cfg.PARENT_LAYER]]
                    log_cfg = True

                item.set_parent_layer(parent, log_cfg)

            if p:
                self.log_item(item)

            self.set_attributes(item, data, p=p)
            self.apply_interfaces(item, data, p=p)

    def set_attributes(self, entity, data, p=False):
        """
        automatically looks up and calls interface methods
            corresponding to the item_cfg data parameters
        """
        keys = [k for k in data]
        order = entity.init_order

        if p:
            print("\nInitializing {}".format(entity))

        # setter methods not listed in 'init_order' will
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

            if hasattr(entity, set_attr):
                if p:
                    print("\t{}".format(set_attr))

                # match value keys from class_dict and model
                value = self.get_value(data[attr])

                # call the setter method with args
                if type(value) is list:
                    args = value
                else:
                    args = [value]
                getattr(entity, set_attr)(*args)

                if p:
                    print("\targs: {}\n".format(args))

            elif attr not in Cfg.INIT_KEYS:
                msg = "no {} method for {}".format(
                    set_attr, entity)

                print(msg)

    def apply_interfaces(self, entity, data, p=False):
        for interface in self.interfaces:
            interface.handle_entity(entity, data, p=p)


class NewApplicationInterface:
    def __init__(self, context, name):
        self.context = context
        self.interface_name = name
        self.get_value = context.get_value

    def handle_entity(self, entity, data, p=False):
        pass

    def add_update_method(self, entity, *args):
        pass

    def call_interface_method(self, entity, *args):
        pass

    def call_entity_method(self, entity, *args):
        pass
