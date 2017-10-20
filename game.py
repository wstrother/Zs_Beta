from sys import exit, argv

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

    def __init__(self, screen, frame_rate, start_env):
        self.environment = start_env
        self.screen = screen
        self.frame_rate = frame_rate

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
            self.main_routine(clock)
            pygame.display.flip()

    def main_routine(self, clock=None):
        # print("\n\n======================")

        # dt value can be printed to stdout or passed to data model
        if clock:
            dt = clock.tick(self.frame_rate) / 1000
            self.environment.model["dt"] = dt
            # print(dt)

        # screen is set to black and passed to environment's main method
        self.screen.fill((0, 0, 0))
        self.environment.main(self.screen)


def start(start_env, class_dict, *apps):
    scr = pygame.display.set_mode(Settings.SCREEN_SIZE)
    fps = Settings.FRAME_RATE

    env = Environment.make_from_cfg(
        start_env, class_dict=class_dict
    )

    for app in apps:
        env.apply_context_interface(
            class_dict, app
        )

    return Game(scr, fps, env)


if __name__ == "__main__":

    if len(argv) > 1:
        start(argv[1], None).main()
    else:
        print("Please specify a start environment")
