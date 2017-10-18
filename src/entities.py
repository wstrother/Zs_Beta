from os.path import join

from src.cfg import save_cfg, format_dict
from src.collections import Group
from src.events import EventHandlerInterface
from src.meters import Clock
from src.controller_io import ControllerIO
from src.context import set_environment_context
from src.resources import load_resource
from zs_globals import Cfg, Zs
from zs_globals import Resources as Dirs


class CfgMetaclass(type):
    """
    This metaclass ensures that the 'initialized' flag
      for new entities is set to true after all __init__
      methods have been called. This flag is used to turn
      on / log changes to public setter methods in the
      entity object's cfg_dict attribute
    """
    def __call__(cls, *args, **kwargs):
        new = type.__call__(cls, *args, **kwargs)
        new.initialized = True

        return new


class Entity(EventHandlerInterface, metaclass=CfgMetaclass):
    """
    Entity is an abstract base class for all objects that will
      make up the application logic layers and sprites. All
      entity objects have a name, position, and size.
    """
    def __init__(self, name):
        self.initialized = False
        self.name = name
        super(Entity, self).__init__()

        # cfg_dict tracks changes to public "setter" methods
        #   and contains "class" entry by default
        self.cfg_dict = {
            "class": self.__class__.__name__
        }

        self.size = 0, 0
        self.position = 0, 0
        self.init_order = []

        self.visible = True
        self.graphics = None
        self.clock = Clock("{}'s clock".format(name))
        self.update_methods = [
            self.clock.tick,
            self.update_graphics
        ]

    def __repr__(self):
        c = self.__class__.__name__
        n = self.name

        return "{}: '{}'".format(c, n)

    # Once initialized, changes to any attribute with
    #   a corresponding setter method are tracked
    def __setattr__(self, key, value):
        super(Entity, self).__setattr__(key, value)

        if self.initialized and hasattr(self, "set_" + key):
            self.log_cfg_change(key, value)

    # automatically generates .cfg syntax arguments for
    #   changes to public setter values
    def log_cfg_change(self, key, value):
        # objects with a "name" attribute will be serialized
        #   by reference to their name and must be defined
        #   elsewhere for proper serialization
        def get_arg_text(i):
            if hasattr(i, "name"):
                return i.name

            else:
                return str(i)

        if type(value) in (list, tuple):
            text = ", ".join([get_arg_text(i) for i in value])

        else:
            text = get_arg_text(value)

        self.cfg_dict[key] = text

        if Zs.PRINT_CFG_LOG:
            print("\t{} value '{}' set to: {}".format(
                self, key, text
            ))

    # returns object data as an "item" entry to be composed
    #   into a .cfg formatted dict
    def get_cfg(self):
        return {self.name: self.cfg_dict}

    def print_cfg(self):
        print(format_dict(self.get_cfg()))

    @property
    def image(self):
        if self.graphics:
            return self.graphics.get_image()

        else:
            return False

    def add_to_list(self, list_name, item):
        l = getattr(self, list_name)

        if item not in l:
            l.append(item)
            setattr(self, list_name, l)

    def move(self, dx, dy, v=1):
        x, y = self.position
        dx *= v
        dy *= v
        self.set_position(x + dx, y + dy)

    def set_size(self, w, h):
        self.size = w, h

    def set_position(self, x, y):
        self.position = x, y

    def update(self):
        for m in self.update_methods:
            m()

    def update_graphics(self):
        if self.graphics:
            self.graphics.update()


class Layer(Entity):
    """
    Layers are the individual component objects of a ZSquirrel
      application. They will typically run update functions that
      act on Groups of Sprite objects, or store/load data.
    Layers should form an application hierarchy with parent and
      sub layers.
    """
    def __init__(self, name):
        super(Layer, self).__init__(name)

        self.sub_layers = []
        self.groups = []
        self.controllers = []
        self.parent_layer = None

        self.update_methods += [
            self.update_controllers,
            self.update_sprites,
            self.update_sub_layers
        ]

    def set_parent_layer(self, layer, log_cfg=True):
        layer.sub_layers.append(self)

        # Because context.py sets layer objects to be
        #   sub_layers of the Environment object by
        #   default, the 'cfg' flag is used to avoid
        #   adding superfluous data to the object's
        #   cfg_dict
        if log_cfg:
            self.parent_layer = layer.name

    def set_groups(self, *groups):
        for g in groups:
            self.add_to_list(Cfg.GROUPS, g)

    def set_controller(self, arg):
        if type(arg) is str:
            cont = ControllerIO.load_controller(arg)

        else:
            name = list(arg.keys())[0]
            cont = ControllerIO.make_controller(
                name, arg[name]
            )

        self.add_to_list(
            "controllers", cont
        )

    def set_controllers(self, *controllers):
        for c in controllers:
            self.set_controller(c)

    def update_controllers(self):
        for c in self.controllers:
            c.update()

    def update_sprites(self):
        for g in self.groups:
            for sprite in g.sprites:
                sprite.update()

    def update_sub_layers(self):
        for layer in self.sub_layers:
            layer.update()

    def draw(self, screen, offset=(0, 0), draw_point=(0, 0)):
        if self.graphics and self.visible:
            screen.blit(
                self.graphics.get_image(), draw_point)

        self.draw_items(
            screen, offset=offset)

    def draw_items(self, canvas, offset=(0, 0)):
        ox, oy = offset

        for group in self.groups:
            for item in group.sprites:
                if item.graphics and item.image and item.visible:

                    x, y = item.position
                    x += ox
                    y += oy

                    canvas.blit(item.image, (x, y))


class Environment(Layer):
    """
    The top most Layer object in an application. Environment
      holds a special attribute dictionary called the "model"
      which allows shared reference to environment data
      including layers, sprite groups, and other generic data.
    """
    def __init__(self, name):
        super(Environment, self).__init__(name)

        self.model = {}

    def get_groups(self):
        model = self.model

        return [
            model[g] for g in model if isinstance(model[g], Group)
            ]

    def get_layers(self):
        model = self.model

        return [
            model[l] for l in model if isinstance(model[l], Layer) and model[l] != self
            ]

    # An Environment object can record it's current state as a
    #   .cfg formatted dict with sections for 'Layers', 'Groups',
    #   and 'Populate'.
    def get_state_as_cfg(self):
        groups = self.get_groups()
        group_dict = {}
        populate_dict = {}

        for group in groups:
            group_dict[group.name] = {}

            for sprite in group.sprites:
                populate_dict.update(sprite.get_cfg())

        layers = self.get_layers()
        layer_dict = {}
        for layer in layers:
            layer_dict.update(layer.get_cfg())

        return {
            Cfg.GROUPS: group_dict,
            Cfg.LAYERS: layer_dict,
            Cfg.POPULATE: populate_dict,
        }

    # Automatically saves object's state as a .cfg file to the
    #   'environments' directory with a the Environment object's
    #   name used as the file name.
    def save_state_as_cfg(self, p=False):
        file_name = self.name.replace(" ", "_") + ".cfg"
        path = join(*Dirs.ENVIRONMENTS + (file_name,))
        save_cfg(self.get_state_as_cfg(), path, p=p)

    @staticmethod
    def make_from_cfg(name, class_dict=None):
        cd = CLASS_DICT.copy()
        if class_dict:
            cd.update(class_dict)

        env = Environment(name)
        cfg = load_resource(name + ".cfg")

        set_environment_context(env, cd, cfg)

        return env

    def main(self, screen):
        for layer in self.sub_layers:
            layer.draw(screen)

        self.update()


class Sprite(Entity):
    """
    Sprite objects should belong to a single Group, which
        will be used by the Environment object to call each
        sprite's update method.
    """
    def __init__(self, name):
        super(Sprite, self).__init__(name)

        self.group = None

    def set_group(self, group):
        self.group = group.name
        group.add_member(self)

# ===================================
# DEFINE THE DEFAULT CLASS DICTIONARY
# ===================================

CLASS_DICT = {
        "Layer": Layer,
        "Environment": Environment,
        "Sprite": Sprite
    }

# ===================================
