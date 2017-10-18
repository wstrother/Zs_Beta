from src.entities import Environment
from src.cfg import format_dict
from game import Game
from src.graphics import AnimationGraphics, TextGraphics
from zs_globals import Settings

import pygame

JSON_DEMO = {
        "data": {
            "Table 1": {
                "a": 1,
                "b": 2,
                "c": "three",
                "d": [4, 5, 6],
                "e": '"seven, eight, nine"',
                "f": ["ten", "eleven", "twelve"],
                "g": [None, False, True]
            }
        }
    }

CFG_STRING = """
# data

Table 1
\ta: 1
\tb: 2
\tc: three
\td: 4, 5, 6
\te: "seven, eight, nine"
\tf: ten, eleven, twelve
\tg: null, false, true
"""

DEMO_ENVIRONMENT = """
# layers

Sprite Layer
\tclass: Layer
\tgroups: Sprite Group

# groups

Sprite Group

# populate

Demo Sprite
\tclass: Sprite
\tadd_to_model
\tsize: 50, 50
\tgroup: Sprite Group
"""


###########################
# DEMO 1: cfg / resources #
###########################

def demo_cfg():
    from src.cfg import get_cfg, format_dict

    s = CFG_STRING

    json = JSON_DEMO

    c = get_cfg(s, ordered=True)

    print("---\nJSON \n{}".format(format_dict(json)))
    print("---\nCFG \n{}".format(format_dict(c)))
    print("---\nJSON == CFG {}".format(c == json))
    assert(c == json)


def demo_resources():
    from src.resources import load_resource
    test = load_resource("test_example.cfg")
    print("---\nTEST_EXAMPLE.CFG \n{}".format(format_dict(test)))


#######################################
# DEMO 2: events / entities / context #
#######################################

def demo_events():
    from src.entities import Sprite

    s = Sprite("Demo Sprite")
    t = Sprite("Demo Sprite 2")

    def print_spawn():
        print("foo")

    def print_die():
        print("die")

    def print_listen():
        print("...listening")

    s.on_spawn = print_spawn
    s.on_die = print_die
    s.on_listen = print_listen
    t.on_listen = print_listen

    e1 = {
        "name": "spawn",
        "duration": 5
    }
    e2 = {
        "name": "pause",
        "duration": 3
    }
    e3 = "die"
    e = s.chain_events(e1, e2, e3)
    s.queue_event(e)
    l = {
        "name": "pause",
        "target": t,
        "response": "listen",
        "temp": True
    }
    s.add_listener(l)
    s.add_listener("pause listen")

    for _ in range(10):
        print("---")
        s.update()


def demo_entities():
    from src.entities import Entity

    e = Entity("Hello World")
    e.print_cfg()
    print("{} size: {}, position: {}".format(
        e, e.size, e.position
    ))
    e.size = 100, 100
    e.move(10, 10)
    e.print_cfg()


def demo_context():
    from src.entities import Sprite, Environment, Layer
    from src.cfg import get_cfg, format_dict
    from src.context import set_environment_context

    class_dict = {
        "Layer": Layer,
        "Environment": Environment,
        "Sprite": Sprite
    }
    env = Environment("Demo Environment")
    set_environment_context(
        env, class_dict,
        get_cfg(DEMO_ENVIRONMENT)
    )

    s = env.model["Demo Sprite"]

    for _ in range(10):
        s.move(10, 10)
        print(format_dict(env.get_state_as_cfg()))


######################################
# DEMO 3: controller / input manager #
######################################

def demo_controller():
    from src.input_manager import InputManager
    from src.controller import Dpad
    im = InputManager()

    scr = pygame.display.set_mode(Settings.SCREEN_SIZE)
    env = Environment.make_from_cfg("demo")
    sl = env.model["Sprite Layer"]
    sl.set_controller("default_controller")

    controller = sl.controllers[0]

    def print_controller():
        for dv in controller.devices:
            if dv.check():
                print(dv)

    sl.update_methods.append(print_controller)

    for d in controller.devices:
        if type(d) != Dpad:
            print(d)
            controller.remap_device(d.name, im.get_mapping())

    Game(scr, 60, env).main()


########################################
# DEMO 4: graphics / animation / style #
########################################

def demo_graphics():
    scr = pygame.display.set_mode(Settings.SCREEN_SIZE)
    env = Environment.make_from_cfg("demo")
    sl = env.model["Sprite Layer"]
    sl.set_controller("default_controller")

    controller = sl.controllers[0]

    ds = env.model["Demo Sprite"]
    gfx = AnimationGraphics.load_from_cfg(ds, "squirrel_animations.cfg")
    ds.graphics = gfx
    label = env.model["Text Sprite"]

    txt = TextGraphics(ds, "Hello World")
    label.graphics = txt

    def set_state():
        a = controller.get_device("A")

        if a.check():
            names = gfx.get_animation_states()
            current = gfx.animation_state
            i = names.index(current)
            i += 1
            i %= len(names)
            gfx.set_animation_state(names[i])
            txt.set_text(names[i])

    sl.update_methods.append(set_state)

    def move():
        dpad = controller.get_device("Dpad")

        if dpad.held:
            dx, dy = dpad.get_direction()
            ds.move(dx, dy, 1.5)

    ds.update_methods.append(move)

    Game(scr, 60, env).main()

if __name__ == "__main__":
    demos = [
        demo_cfg,
        demo_resources,
        demo_events,
        demo_entities,
        demo_context,
        demo_controller,
        demo_graphics
    ]

    from sys import argv

    if len(argv) > 1:
        args = argv[1:]
        demo_names = ["demo_" + arg for arg in args]

        demos = filter(lambda d: d.__name__ in demo_names, demos)

    for demo in demos:
        print("{}\n{:*^50}\n{}".format(
            "*" * 50,
            demo.__name__,
            "*" * 50
        ))
        demo()
