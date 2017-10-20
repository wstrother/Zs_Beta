from zs_globals import Cfg
from src.collections import Group


def set_environment_context(env, class_dict, cfg, p=False):
    update_model(class_dict, cfg, env)
    add_layers(class_dict, cfg, env, p=p)
    populate(class_dict, cfg, env, p=p)


def get_spawn_method(class_dict, cls):
    """
    returns callable method for entity objects
      from imported modules in class_dict
    """
    def spawn(name):
        return class_dict[cls](name)

    return spawn


def update_model(class_dict, cfg, environment, p=False):
    """
    updates environment model {} object based
          on imported class_dict and cfg data
    """
    model = environment.model

    if p:
        print("\nUpdating Model for {}".format(environment))

    for section in cfg:
        current = cfg[section]

        for name in current:
            entry = current[name]

            if section == Cfg.GROUPS:
                item = Group(name)

            elif section in Cfg.CONSTRUCTOR_SECTIONS:
                item = get_spawn_method(
                    class_dict, entry[Cfg.CLASS_KEYWORD]
                    )(name)

            else:
                item = value_from_key_lookup(
                    name, class_dict, model
                )

            if section != Cfg.POPULATE:
                if p:
                    print("\t{} added to model".format(name))
                model[name] = item


def add_layers(class_dict, log_cfg, environment, p=False):
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

        init_item(
            class_dict, model,
            layer, item_cfg, p=p
        )


def populate(class_dict, cfg, environment, p=False):
    """
    populates an Environment object with sprite objects
        and adds them to designated groups
    """
    model = environment.model
    pd = cfg[Cfg.POPULATE]

    for name in pd:
        # Add / initialize sprite objects for environment
        item_cfg = pd[name]

        spawn = get_spawn_method(
            class_dict, item_cfg[Cfg.CLASS_KEYWORD])

        item = spawn(name)

        init_item(
            class_dict, model,
            item, item_cfg, p=p
        )

        if Cfg.ADD_TO_MODEL in item_cfg:
            model[item.name] = item
            item.cfg_dict[Cfg.ADD_TO_MODEL] = True


def init_item(class_dict, model, item, item_cfg, p=False):
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
            value = value_from_key_lookup(
                item_cfg[attr], class_dict, model)

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


def value_from_key_lookup(value, class_dict, model):
    """
    looks up corresponding keys to data argument in
      the imported class_dict and data model
    """
    def get(k, cd, m):
        if k == Cfg.MODEL:
            return m

        if k in cd:
            return cd[k]

        if k in m:
            return m[k]

        else:
            return k

    if type(value) is list:
        new = []
        for item in value:
            new.append(
                get(item, class_dict, model)
            )

        return new

    elif type(value) is dict:
        for key in value:
            if value[key] is True:
                value[key] = get(key, class_dict, model)

        return value

    else:
        return get(value, class_dict, model)
