from collections import OrderedDict
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

        self.interfaces = []
        for interface in interfaces:
            self.interfaces.append(
                interface(self)
            )

        self.model = {}

    def get_environment(self, name):
        env = Environment(name)
        cfg = load_resource(name)

        self.set_environment_context(cfg, env, p=True)

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
        self.model = {"environment": env}

        groups = cfg.pop("groups")
        layers = cfg.pop("layers")
        sprites = cfg.pop("sprites")
        data = cfg

        entities = OrderedDict()
        entities.update(layers)
        entities.update(sprites)

        # add "empty" entities to model: groups, layers, sprites
        self.add_groups(groups)

        for name in entities:
            layer = name in layers
            self.add_entities(
                name, entities[name], layer=layer
            )

        # add "data" sections to model

        for section in data:
            self.update_model(data[section], p=p)

        # set attributes on cfg entities
        # apply interface methods to cfg entities

        for name in entities:
            entity = self.model[name]
            data = entities[name]

            self.set_attributes(entity, data)
            self.apply_interfaces(entity, data)

    def update_model(self, section, p=False):
        for name in section:
            item = section[name]
            for key in item:
                item[key] = self.get_value(item[key])

            add_to_model = item.get(Cfg.ADD_TO_MODEL, True)
            if add_to_model:
                self.model[name] = item

                if p:
                    self.log_item(item, name=name)

    def add_groups(self, section, p=False):
        for group_name in section:
            group = Group(group_name)
            self.model[group_name] = group

            if p:
                self.log_item(group)

    def add_entities(self, name, data, layer=False, p=False):
        item = self.get_spawn_method(
            data[Cfg.CLASS_KEYWORD]
        )(name)
        self.model[name] = item

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

    @staticmethod
    def get_init_order(data, order):
        keys = [k for k in data]

        attrs = [
                    o for o in order if o in keys
                    ] + [
                    k for k in keys if k not in order
                    ]

        return attrs

    def set_attributes(self, entity, data, p=False):
        for attr in self.get_init_order(data, entity.init_order):
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
        for interface in [i for i in self.interfaces if i.name in data]:
            section_name = data[interface.name]

            if ".json" in section_name:
                section = load_resource(section_name)
            else:
                section = self.model[section_name]

            interface.apply_to_entity(entity, section, p=p)


class ApplicationInterface:
    def __init__(self, context, name):
        self.context = context
        self.name = name
        self.get_value = context.get_value
        self.init_order = []

    def log_item(self, entity, method_name, *args):
        print("{} applying {} to {} with args: {}".format(
            self.name, method_name, entity, args
        ))

    def apply_to_entity(self, entity, data, p=False):
        for method_name in self.context.get_init_order(data, self.init_order):
            value = self.get_value(data[method_name])
            if type(value) is not list:
                args = [value]
            else:
                args = value

            self.handle_data_item(
                entity, method_name, *args
            )

            if p:
                self.log_item(entity, method_name, *args)

    def handle_data_item(self, entity, method_name, *args):
        # self.add_update_method(entity, method_name, *args):
        # self.call_method(entity, method_name, *args):
        # self.call_method_on_entity(entity, method_name, *args)
        pass

    def add_update_method(self, entity, method_name, *args):
        m = self.get_interface_method(
            entity, method_name
        )

        if m:
            def interface_update_method():
                m(*args)

            entity.update_methods.append(interface_update_method)

    def call_method(self, entity, method_name, *args):
        m = self.get_interface_method(
            entity, method_name
        )

        if m:
            m(*args)

    def call_method_on_entity(self, entity, method_name, *args):
        m = self.get_interface_method(
            entity, method_name
        )

        if m:
            m(entity, *args)

    def get_interface_method(self, entity, method_name):
        m = None
        i_method = getattr(self, method_name, None)
        e_method = getattr(entity, method_name, None)

        if i_method and callable(i_method):
            m = i_method
        elif e_method and callable(e_method):
            m = e_method

        return m
