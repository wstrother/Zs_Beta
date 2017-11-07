from sys import exit

import pygame

from src.entities import Environment
from zs_globals import Settings

pygame.init()
pygame.mixer.quit()
pygame.mixer.init(buffer=256)


class Game:
    """
    The Game object is used to sync a game environment / data model with a display surface
        and update them both at a regular interval.
    """

    def __init__(self, screen, frame_rate, start_env, context):
        self.environment = None
        self.screen = screen
        self.frame_rate = frame_rate
        self.context = context

        self.set_environment(start_env)

    '''This method is necessary to poll and clear the Pygame events queue, as well as
    checking for QUIT events to close the program'''
    @staticmethod
    def poll_events():
        # PYGAME CHOKE POINT

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

    def main(self):
        # print("GAME INITIALIZED\nmain() called")
        # PYGAME CHOKE POINT

        clock = pygame.time.Clock()         # clock object used to set max frame_rate

        while True:
            self.poll_events()
            self.update_environment(clock)
            pygame.display.flip()

    def update_environment(self, clock=None):
        # print("\n\n======================")

        # dt value can be printed to stdout or passed to data model
        if clock:
            dt = clock.tick(self.frame_rate) / 1000
            self.environment.model["dt"] = dt
            # print(dt)

        # screen is set to black and passed to environment's main method
        self.screen.fill((0, 0, 0))
        self.environment.main(self.screen)

        if self.environment.transition:
            self.handle_transition()

    def handle_transition(self):
        old = self.environment
        t = old.transition

        if "exit" in t:
            exit()

        else:
            self.set_environment(
                t["environment"]
            )

            if not t.get("to_parent", False):
                self.environment.return_to = old
                old.transition = {}

    def set_environment(self, env):
        if not type(env) is Environment:
            env = self.context.get_environment(env)

        # if not env.spawned:
        #     self.context.apply_interfaces(env)

        self.environment = env


def start(env, context):
    scr = pygame.display.set_mode(Settings.SCREEN_SIZE)
    fps = Settings.FRAME_RATE

    return Game(scr, fps, env, context)
