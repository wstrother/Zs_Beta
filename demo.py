from src.entities import Environment
from src.cfg import format_dict
from game import Game
from src.graphics import ImageGraphics
from zs_globals import Settings

import pygame

env = Environment.make_from_cfg("demo")

sl = env.model["Sprite Layer"]
sl.set_controller("default_controller")

ds = env.model["Demo Sprite"]
r = (0, 0), (50, 50)
gfx = ImageGraphics(ds, "squirrel.gif", r)
ds.graphics = gfx

print(format_dict(
    env.get_state_as_cfg())
)


# def print_sprite():
#     output = ["."] * 20
#     output[ds.position[0] % 20] = "X"
#     output = "".join(output)
#
#     c = sl.controllers[0]
#     dpad = c.get_device("Dpad")
#
#     if dpad.held:
#         print(output)
#
# sl.update_methods.append(print_sprite)


def move():
    c = sl.controllers[0]
    dpad = c.get_device("Dpad")

    if dpad.held:
        dx, dy = dpad.get_direction()
        ds.move(dx, dy, 5)


ds.update_methods.append(move)

scr = pygame.display.set_mode(Settings.SCREEN_SIZE)
g = Game(scr, 60, env)
g.main()
