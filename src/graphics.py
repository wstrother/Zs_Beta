from src.resources import load_resource, get_font
from pygame import SRCALPHA
from pygame.surface import Surface
from pygame.rect import Rect
from src.meters import Meter

# pygame.font.init()
# BORDER_CORNER_CHOICES = "abcd"
# RECT_DRAW_WIDTH = 5
# RECT_DRAW_COLOR = 255, 0, 0


class Graphics:
    PRE_RENDERS = {}

    def __init__(self, entity):
        self.entity = entity
        self.image = None

    def update(self):
        pass

    def get_image(self):
        return self.image


class ImageGraphics(Graphics):
    def __init__(self, entity, file_name, sub=False):
        super(ImageGraphics, self).__init__(entity)

        image = load_resource(file_name)
        self.set_colorkey(image)

        if not sub:
            self.image = image
        else:
            position, size = sub
            self.image = self.make_sub_image(
                image, position, size
            )

    @staticmethod
    def make_sub_image(image, position, size):
        return image.subsurface(Rect(position, size))

    @staticmethod
    def set_colorkey(img, pixel=(0, 0)):
        # PYGAME CHOKE POINT

        img.set_colorkey(
            img.get_at(pixel)
        )


class AnimationGraphics(ImageGraphics):
    def __init__(self, entity, file_name, animations):
        super(AnimationGraphics, self).__init__(entity, file_name)
        self.animations = animations
        self.animation_state = ""
        self.animation_meter = Meter(
            "Animation Meter for {}".format(entity),
            0, 0, 1
        )
        self.image_sets = self.get_image_sets(animations)

    def get_image_sets(self, animations):
        sets = {}

        for a in animations.values():
            sets[a.name] = [
                self.make_sub_image(
                    self.image,
                    a.get_cell_position(i),
                    a.cell_size
                ) for i in range(a.length - 1)
            ]

        return sets

    def set_animation_state(self, state):
        self.animation_state = state
        a = self.get_animation(state)

        self.animation_meter.reset()
        self.animation_meter.maximum = ((a.length - 1) * a.frame_rate) - 1

    def get_image(self):
        a = self.get_animation()

        if a:
            i = self.animation_meter.value // a.frame_rate
            return self.image_sets[
                self.animation_state
            ][i]

    def get_animation(self, state=None):
        if not state:
            state = self.animation_state

        animations = self.animations
        default = animations.get("default", None)

        return animations.get(state, default)

    def update(self):
        self.animation_meter.next()

    @staticmethod
    def load_from_cfg(entity, file_name):
        d = load_resource(file_name, "animations")
        image = d["info"]["sprite_sheet"]

        animations = {}
        for name in d:
            if name != "info":
                animations[name] = Animation(name, d)

        gfx = AnimationGraphics(
            entity, image, animations
        )
        gfx.set_animation_state(d["info"]["default"])

        return gfx


class Animation:
    def __init__(self, name, d):
        self.name = name
        self.frames = list(d[name].values())

        self.frame_rate = d["info"]["frame_rate"]
        self.cell_size = d["info"]["size"]
        self.length = len(self.frames)

    def get_cell_position(self, i):
        x, y = self.frames[i]
        w, h = self.cell_size
        x *= w
        y *= h

        return x, y


DEFAULT_STYLE = {
    "font_name": "courier-new",
    "font_size": 15,
    "font_color": (255, 255, 255),
    "text_buffer": 5,
    "text_cutoff": 20,
    "text_newline": False,
}


class TextGraphics(Graphics):
    def __init__(self, entity, text):
        if type(text) not in (str, list):
            text = str(text)
        self.text = text

        super(TextGraphics, self).__init__(entity)
        self.image = self.make_image()

    def make_image(self):
        if getattr(self.entity, "style", False):
            style = self.entity.style
        else:
            style = DEFAULT_STYLE

        font_name = style["font_name"]
        size = style["font_size"]
        bold = style.get("bold", False)
        italic = style.get("italic", False)
        color = style["font_color"]
        buffer = style["text_buffer"]
        cutoff = style.get("text_cutoff", None)
        nl = style.get("text_newline", True)

        font = get_font(
            font_name, size, bold, italic)

        image = self.make_text_image(
            self.text, font, color, buffer,
            cutoff=cutoff, nl=nl)

        return image

    @staticmethod
    def get_text(text, cutoff, nl):
        if type(text) == str:
            text = [text]

        for i in range(len(text)):
            line = str(text[i])
            line = line.replace("\t", "    ")
            line = line.replace("\r", "\n")
            if not nl:
                line = line.replace("\n", "")
            text[i] = line

        new_text = []

        for line in text:
            if cutoff:
                new_text += TextGraphics.format_text(
                    line, cutoff)
            else:
                if nl:
                    new_text += line.split("\n")
                else:
                    new_text += [line]

        if not new_text:
            new_text = [" "]

        return new_text

    @staticmethod
    def make_text_image(text, font, color, buffer,
                        cutoff=0, nl=True):
        text = TextGraphics.get_text(
            text, cutoff, nl)

        line_images = []
        for line in text:
            line_images.append(
                font.render(line, 1, color))

        widest = sorted(line_images, key=lambda l: -1 * l.get_size()[0])[0]
        line_height = (line_images[0].get_size()[1] + buffer)
        w, h = widest.get_size()[0], (line_height * len(line_images)) - buffer

        sprite_image = Surface(
            (w, h), SRCALPHA, 32
        )

        for i in range(len(line_images)):
            image = line_images[i]
            y = line_height * i
            sprite_image.blit(image, (0, y))

        return sprite_image

    @staticmethod
    def format_text(text, cutoff):
        f_text = []
        last_cut = 0

        for i in range(len(text)):
            char = text[i]
            done = False

            if char == "\n" and i - last_cut > 0:
                f_text.append(text[last_cut:i])
                last_cut = i + 1
                done = True

            if i == len(text) - 1:
                f_text.append(text[last_cut:])
                done = True

            if i - last_cut >= cutoff and not done:
                if char == " ":
                    f_text.append(text[last_cut:i])
                    last_cut = i + 1
                else:
                    search = True
                    x = i
                    while search:
                        x -= 1
                        if text[x] == " ":
                            next_line = text[last_cut:x]
                            last_cut = x + 1
                            f_text.append(next_line)
                            search = False
                        else:
                            if x <= last_cut:
                                next_line = text[last_cut:i]
                                last_cut = i
                                f_text.append(next_line)
                                search = False

        return f_text
