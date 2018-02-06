from pygame import SRCALPHA, draw, transform
from pygame.rect import Rect
from pygame.surface import Surface

from src.meters import Meter
from src.resources import load_resource, get_font
from zs_globals import Settings, DefaultUI


class Graphics:
    PRE_RENDERS = {}

    def __init__(self, entity):
        self.entity = entity
        self.image = None

    def update(self):
        pass

    def get_image(self):
        return self.image

    def reset_image(self):
        if self.entity.spawned:
            self.image = self.make_image()
            if self.image:
                self.entity.set_size(
                    *self.image.get_size()
                )

    def make_image(self):
        pass


class ImageGraphics(Graphics):
    def __init__(self, entity, file_name, sub=False, scale=1):
        super(ImageGraphics, self).__init__(entity)

        self.sub = sub
        self.scale = scale
        self.file_name = file_name

    def make_image(self):
        image = load_resource(self.file_name)
        scale = self.scale
        if scale != 1:
            image = self.scale_image(image, scale)

        if not self.sub:
            return image

        else:
            (x, y), (w, h) = self.sub
            x *= scale
            y *= scale
            w *= scale
            h *= scale
            return self.make_sub_image(
                image, (x, y), (w, h)
            )

    @staticmethod
    def flip_image(image, x_bool, y_bool):
        return transform.flip(image, x_bool, y_bool)

    @staticmethod
    def scale_image(image, scale):
        w, h = image.get_size()
        w *= scale
        h *= scale
        return transform.scale(image, (w, h))

    @staticmethod
    def make_sub_image(image, position, size):
        # PYGAME CHOKE POINT
        return image.subsurface(Rect(position, size))

    @staticmethod
    def set_colorkey(img, pixel=(0, 0)):
        # PYGAME CHOKE POINT

        img.set_colorkey(
            img.get_at(pixel)
        )


class TextGraphics(Graphics):
    def __init__(self, entity):
        super(TextGraphics, self).__init__(entity)

    def make_image(self):
        style = self.entity.style

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

        args = (
            self.entity.get_text(),
            font, tuple(color), buffer
        )
        kwargs = dict(cutoff=cutoff, nl=nl)
        h_key = hash(args + (cutoff, nl))

        if h_key in Graphics.PRE_RENDERS:
            return Graphics.PRE_RENDERS[h_key]

        else:
            image = self.make_text_image(
                *args, **kwargs)
            Graphics.PRE_RENDERS[h_key] = image

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


class RectGraphics(Graphics):
    def make_image(self):
        entity = self.entity
        color = entity.style.get(
            "draw_color", DefaultUI.RECT_DRAW_COLOR)

        return self.get_rect_image(
            entity.size, color, DefaultUI.RECT_DRAW_WIDTH)

    @staticmethod
    def get_rect_image(size, color, draw_width):
        h_key = hash(("rect", size, color, draw_width))
        if h_key in Graphics.PRE_RENDERS:
            return Graphics.PRE_RENDERS[h_key]

        else:
            # PYGAME CHOKE POINT

            rect = Rect((0, 0), size)
            image = Surface(
                size, SRCALPHA, 32)
            draw.rect(
                image, color, rect, draw_width)

            Graphics.PRE_RENDERS[h_key] = image
            return image

    @staticmethod
    def get_circle_image(radius, color, draw_width):
        h_key = hash(("circle", radius, color, draw_width))
        if h_key in Graphics.PRE_RENDERS:
            return Graphics.PRE_RENDERS[h_key]

        else:
            # PYGAME CHOKE POINT

            size = 2 * radius, 2 * radius
            position = radius, radius

            image = Surface(
                size, SRCALPHA, 32)

            draw.circle(
                image, color, position,
                radius, draw_width)

            Graphics.PRE_RENDERS[h_key] = image
            return image


class ContainerGraphics(Graphics):
    def __init__(self, entity):
        super(ContainerGraphics, self).__init__(entity)

        self.bg_image = None
        self.corner_image = None
        self.h_side_image = None
        self.v_side_image = None
        self.border_size = 0, 0
        self.get_style_attributes()

    def get_style_attributes(self):
        style = self.entity.style
        border_images = style["border_images"]
        h_side, v_side, corner = border_images
        self.h_side_image = load_resource(h_side)
        self.v_side_image = load_resource(v_side)
        self.corner_image = load_resource(corner)
        self.border_size = self.corner_image.get_size()

    def make_image(self, bg_color=False):
        entity = self.entity
        size = entity.size
        style = entity.style

        if not bg_color:
            # BG COLOR
            if style["bg_color"]:
                bg_color = style["bg_color"]
            else:
                bg_color = 0, 0, 0

        image = self.make_color_image(
            size, bg_color)

        # BG TILE IMAGE
        if style.get("bg_image", None):
            self.bg_image = load_resource(style["bg_image"])
            image = self.tile(
                style["bg_image"], image)

        # BORDERS
        if style.get("border", None):
            border_images = style["border_images"]
            sides = style["border_sides"]
            corners = style["border_corners"]

            image = self.make_border_image(
                border_images, image, sides, corners
            )

        # BORDER ALPHA TRIM
        if style.get("alpha_color", None):
            image = self.convert_colorkey(
                image, (255, 0, 0)
            )

        return image

    @staticmethod
    def tile(image_name, surface):
        # PYGAME CHOKE POINT

        if image_name not in Graphics.PRE_RENDERS:
            bg_image = load_resource(image_name)
            sx, sy = Settings.SCREEN_SIZE    # pre render the tiled background
            sx *= 2                          # to the size of a full screen
            sy *= 2
            pr_surface = Surface(
                (sx, sy), SRCALPHA, 32)

            w, h = pr_surface.get_size()
            img_w, img_h = bg_image.get_size()

            for x in range(0, w + img_w, img_w):
                for y in range(0, h + img_h, img_h):
                    pr_surface.blit(bg_image, (x, y))

            Graphics.PRE_RENDERS[image_name] = pr_surface

        full_bg = Graphics.PRE_RENDERS[image_name]      # return a subsection of the full
        #                                               # pre rendered background
        r = surface.get_rect().clip(full_bg.get_rect())
        blit_region = full_bg.subsurface(r)
        surface.blit(blit_region, (0, 0))

        return surface

    @staticmethod
    def make_color_image(size, color):
        # PYGaME CHOKE POINT

        s = Surface(size).convert()
        if color:
            s.fill(color)
        else:
            s.set_colorkey(s.get_at((0, 0)))

        return s

    @staticmethod
    def convert_colorkey(surface, colorkey):
        surface.set_colorkey(colorkey)

        return surface

    @staticmethod
    def make_border_image(border_images, surface, sides, corners):
        h_side_image, v_side_image, corner_image = border_images

        draw_corners = ContainerGraphics.draw_corners
        full_h_side = ContainerGraphics.get_h_side(h_side_image)
        full_v_side = ContainerGraphics.get_v_side(v_side_image)

        w, h = surface.get_size()

        if "l" in sides:
            surface.blit(full_h_side, (0, 0))

        if "r" in sides:
            h_offset = w - full_h_side.get_size()[0]
            surface.blit(transform.flip(
                full_h_side, True, False), (h_offset, 0))

        if "t" in sides:
            surface.blit(full_v_side, (0, 0))

        if "b" in sides:
            v_offset = h - full_v_side.get_size()[1]
            surface.blit(transform.flip(
                full_v_side, False, True), (0, v_offset))

        if corners:
            draw_corners(corner_image, surface, corners)

        return surface

    @staticmethod
    def get_h_side(image):
        return ContainerGraphics.get_full_side_image(image, "h")

    @staticmethod
    def get_v_side(image):
        return ContainerGraphics.get_full_side_image(image, "v")

    @staticmethod
    def get_full_side_image(image_name, orientation):
        if image_name not in ContainerGraphics.PRE_RENDERS:
            image = load_resource(image_name)
            iw, ih = image.get_size()

            h, v = "hv"
            size = {h: (iw, Settings.SCREEN_SIZE[1]),
                    v: (Settings.SCREEN_SIZE[0], iw)}[orientation]
            pr_surface = Surface(
                size, SRCALPHA, 32)

            span = {h: range(0, size[1], ih),
                    v: range(0, size[0], iw)}[orientation]

            for i in span:
                position = {h: (0, i),
                            v: (i, 0)}[orientation]
                pr_surface.blit(image, position)

            ContainerGraphics.PRE_RENDERS[image_name] = pr_surface

        return ContainerGraphics.PRE_RENDERS[image_name]

    @staticmethod
    def draw_corners(image_name, surface, corners):
        corner_image = load_resource(image_name)
        w, h = surface.get_size()
        cw, ch = corner_image.get_size()
        a, b, c, d = DefaultUI.BORDER_CORNER_CHOICES
        locations = {a: (0, 0),
                     b: (w - cw, 0),
                     c: (0, h - ch),
                     d: (w - cw, h - ch)}

        for corner in corners:
            surface.blit(ContainerGraphics.get_corner(corner_image, corner), locations[corner])

    @staticmethod
    def get_corner(img, string):
        a, b, c, d = DefaultUI.BORDER_CORNER_CHOICES
        flip = transform.flip
        corner = {a: lambda i: i,
                  b: lambda i: flip(i, True, False),
                  c: lambda i: flip(i, False, True),
                  d: lambda i: flip(i, True, True)}[string](img)

        return corner


class AnimationGraphics(Graphics):
    def __init__(self, entity, image_sets):
        super(AnimationGraphics, self).__init__(entity)

        self.image_sets = image_sets
        self.animation_meter = Meter(
            "Animation Meter for {}".format(entity),
            0, 0, 1
        )

    def get_image(self):
        state = self.entity.animation_state
        i = self.animation_meter.value

        if state:
            return self.image_sets[state][i]

    def reset_image(self):
        pass

    def update(self):
        self.animation_meter.next()

    def reset_animation(self):
        state = self.entity.animation_state
        i = len(self.image_sets[state]) - 1

        self.animation_meter.reset()
        self.animation_meter.maximum = i

