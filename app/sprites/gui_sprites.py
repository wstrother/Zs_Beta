from src.entities import Sprite
from src.flex import MemberTable
from src.graphics import TextGraphics, RectGraphics
from app.interfaces.controller_interface import ControllerInterface

DEFAULT_STYLE = {
    "font_name": "courier-new",
    "font_size": 15,
    "font_color": (255, 255, 255),
    "text_buffer": 5,
    "text_cutoff": 20,
    "text_newline": False,
    "border_size": (5, 5),
    "buffers": (5, 5),
    "aligns": ("r", "b")
}


class GuiSprite(Sprite):
    def __init__(self, name):
        super(GuiSprite, self).__init__(name)
        self._style = DEFAULT_STYLE.copy()

    @property
    def style(self):
        return self._style

    @style.setter
    def style(self, value):
        self._style.update(value)


class BlockSprite(GuiSprite):
    def __init__(self, name):
        super(BlockSprite, self).__init__(name)
        self.init_order += [
            "members", "group", "size", "position"
        ]
        self.members = MemberTable()
        self.graphics = RectGraphics(self)
        self.last = None

        self.update_methods += [
            self.update_pointer
        ]

    def update_pointer(self):
        ControllerInterface.move_pointer(self)
        ControllerInterface.check_activation(self)
        self.last = self.members.active_member

    def move_pointer(self, x, y):
        self.members.move_pointer(x, y)

        active = self.members.active_member
        last = self.last

        if last != active:
            self.handle_select(active)
            if last:
                self.handle_deselect(last)

    @staticmethod
    def handle_select(sprite):
        sprite.queue_event("select")

    @staticmethod
    def handle_deselect(sprite):
        sprite.queue_event("deselect")

    @staticmethod
    def handle_activation(sprite):
        sprite.queue_event("activate")

    def set_members(self, table):
        new_table = []
        for key in sorted(table.keys()):
            new_row = []

            for item in table[key]:
                new_row.append(item)

            new_table.append(new_row)

        self.members.table = self.get_sprites_from_table(new_table)
        self.set_size(*self.size)
        self.set_table_positions()

    def set_table_positions(self):
        style = self.style
        self.members.set_member_position(
            self.position, self.size,
            style["border_size"],
            style["buffers"],
            style["aligns"]
        )
        self.reset_image()

    def get_members(self):
        return self.members.member_list

    def get_option(self, text):
        if type(text) is str:
            for sprite in self.members.member_list:
                if sprite.text == text:

                    return sprite

        elif type(text) is int:
            i = text
            return self.members.member_list[i]

    def set_group(self, group):
        super(BlockSprite, self).set_group(group)

        for sprite in self.get_members():
            sprite.set_group(group)

    def set_position(self, x, y):
        super(BlockSprite, self).set_position(x, y)

        self.set_table_positions()

    def set_size(self, w, h):
        super(BlockSprite, self).set_size(w, h)

        style = self.style
        self.size = self.members.adjust_size(
            self.size, style["border_size"],
            style["buffers"]
        )
        self.set_table_positions()
        self.reset_image()

    def reset_image(self):
        self.graphics.image = self.graphics.make_image()

    @staticmethod
    def get_sprites_from_table(table):
        new_table = []

        for row in table:
            new_row = []
            for item in row:
                if item is not None:
                    ts = TextSprite(str(item))
                    ts.set_text(str(item))
                    new_row.append(ts)
                else:
                    new_row.append(None)

            new_table.append(new_row)

        return new_table

    def on_spawn(self):
        self.handle_select(self.members.active_member)


class TextSprite(GuiSprite):
    def __init__(self, name):
        super(TextSprite, self).__init__(name)
        self.graphics = TextGraphics(self, "")
        self.text = ""

    def set_text(self, text):
        self.text = text
        self.graphics.set_text(text)
        self.set_size(
            *self.graphics.get_image().get_size()
        )

    def on_select(self):
        self.style = {"font_color": (0, 255, 0)}
        self.set_text(self.text)

    def on_deselect(self):
        self.style = {"font_color": (255, 255, 255)}
        self.set_text(self.text)

    def on_activate(self):
        print(self.text)
