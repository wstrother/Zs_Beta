import pygame
from math import sqrt


def get_distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    dx = abs(x1 - x2)
    dy = abs(y1 - y2)

    return sqrt(dx**2 + dy**2)


class Rect:
    RECT_COLOR = 0, 255, 125

    def __init__(self, size, position):
        self.size = size
        self.position = position

    def __repr__(self):
        return "Rect: {}, {}".format(self.size, self.position)

    def draw(self, screen, offset=(0, 0)):
        r = self.pygame_rect
        color = self.RECT_COLOR

        r.x += offset[0]
        r.y += offset[1]

        pygame.draw.rect(
            screen, color,
            r, 1
        )

    def move(self, value):
        dx, dy = value
        x, y = self.position
        x += dx
        y += dy
        self.position = x, y

    @property
    def pygame_rect(self):
        r = pygame.Rect(
            self.position, self.size
        )

        return r

    @property
    def clip(self):
        return self.pygame_rect.clip

    def copy(self):
        return self.get_from_pygame_rect(self.pygame_rect.copy())

    @staticmethod
    def get_from_pygame_rect(rect):
        return Rect(rect.size, rect.topleft)

    @property
    def width(self):
        return self.size[0]

    @width.setter
    def width(self, value):
        self.size = value, self.size[1]

    @property
    def height(self):
        return self.size[1]

    @height.setter
    def height(self, value):
        self.size = self.size[0], value

    @property
    def right(self):
        return self.position[0] + self.width

    @right.setter
    def right(self, value):
        dx = value - self.right
        self.move((dx, 0))

    @property
    def left(self):
        return self.position[0]

    @left.setter
    def left(self, value):
        dx = value - self.left
        self.move((dx, 0))

    @property
    def top(self):
        return self.position[1]

    @top.setter
    def top(self, value):
        dy = value - self.top
        self.move((0, dy))

    @property
    def bottom(self):
        return self.top + self.height

    @bottom.setter
    def bottom(self, value):
        dy = value - self.bottom
        self.move((0, dy))

    @property
    def midleft(self):
        return self.left, self.top + (self.height / 2)

    @property
    def topleft(self):
        return self.left, self.top

    @property
    def midtop(self):
        return self.left + (self.width / 2), self.top

    @property
    def topright(self):
        return self.right, self.top

    @property
    def midright(self):
        return self.right, self.top + (self.height / 2)

    @property
    def bottomleft(self):
        return self.left, self.bottom

    @property
    def midbottom(self):
        return self.left + (self.width / 2), self.bottom

    @property
    def bottomright(self):
        return self.right, self.bottom

    @property
    def center(self):
        return (self.left + (self.width / 2),
                self.top + (self.height / 2))

    @center.setter
    def center(self, value):
        x, y = value
        x -= self.width / 2
        y -= self.height / 2

        self.position = x, y

    def get_rect_collision(self, other):
        try:
            collision = self.clip(other.pygame_rect)

            if not (collision.width or collision.height):
                return False

            else:
                return collision.center

        except ValueError:
            return False

    def get_circle_collision(self, radius, position):
        points = [
            self.center,
            self.topleft,
            self.topright,
            self.bottomleft,
            self.bottomright
        ]

        for point in points:
            d = get_distance(position, point)

            if d <= radius:
                return point
