from src.resources import load_resource
from pygame.rect import Rect

# pygame.font.init()
# BORDER_CORNER_CHOICES = "abcd"
# RECT_DRAW_WIDTH = 5
# RECT_DRAW_COLOR = 255, 0, 0


class Graphics:
    PRE_RENDERS = {}

    def __init__(self, entity):
        self.entity = entity
        self.image = None

        self.reset_image()

    def update(self):
        pass

    def get_image(self):
        return self.image

    def make_image(self):
        pass

    def reset_image(self):
        self.image = self.make_image()

        # if self.entity.rect:
        #     self.entity.rect.size = self.image.get_size()

    def dying_graphics(self, timer):
        ratio = 1 - timer.get_ratio()
        self.image.set_alpha(255 * ratio)


class ImageGraphics(Graphics):
    def __init__(self, entity, file_name, sub=False):
        self.file_name = file_name

        if sub:
            self.sub_section = sub
        else:
            self.sub_section = []

        super(ImageGraphics, self).__init__(entity)

    def make_image(self):
        image = load_resource(self.file_name)
        self.set_colorkey(image)

        if self.sub_section:
            image = image.subsurface(Rect(
                *self.sub_section
            ))

        return image

    @staticmethod
    def set_colorkey(img, pixel=(0, 0)):
        # PYGAME CHOKE POINT

        img.set_colorkey(
            img.get_at(pixel)
        )
