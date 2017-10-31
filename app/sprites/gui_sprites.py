from src.entities import Sprite
from src.flex import MemberTable
from src.graphics import TextGraphics, ContainerGraphics
from app.interfaces.controller_interface import ControllerInterface

DEFAULT_STYLE = {
    "font_name": "courier-new",
    "font_size": 15,
    "font_color": (255, 255, 255),
    "text_buffer": 5,
    "text_cutoff": 100,
    "text_newline": False,
    "border_size": (5, 5),
    "buffers": (5, 5),
    "aligns": ("c", "t"),
    "bg_color": (0, 0, 255),
    "bg_image": "bg.png",
    "border": True,
    "bold": True,
    "border_images": ("h_side.png", "v_side.png", "corner.png"),
    "border_sides": "tlrb",
    "border_corners": "abcd",
    "alpha_color": (255, 0, 0)
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

    def set_size(self, w, h):
        old = self.size
        super(GuiSprite, self).set_size(w, h)
        new = self.size

        if old != new:
            self.handle_event({
                "name": "change_size",
                "size": [w, h]
            })

    def set_position(self, x, y):
        old = self.position
        super(GuiSprite, self).set_position(x, y)
        new = self.position

        if old != new:
            self.handle_event({
                "name": "change_position",
                "position": [x, y]
            })


class BlockSprite(GuiSprite):
    def __init__(self, name):
        super(BlockSprite, self).__init__(name)
        self.init_order += [
            "members", "group", "size", "position"
        ]
        self.members = MemberTable()
        self.members.select_function = self.selectable

        self.graphics = ContainerGraphics(self)

        self.last = None
        self.pointer_paused = False

        self.update_methods += [
            self.update_pointer
        ]

    @staticmethod
    def selectable(option):
        return bool(getattr(
            option, "on_select", False
        ))

    def update_pointer(self):
        if not self.pointer_paused:
            ControllerInterface.move_pointer(self)

        ControllerInterface.check_activation(self)
        self.last = self.members.active_member

        if self.members.member_list:
            if not self.selectable(
                    self.members.active_member
            ):
                self.move_pointer(1, 1)

    def move_pointer(self, x, y):
        if self.members.member_list:
            self.members.move_pointer(x, y)

            active = self.members.active_member
            last = self.last

            if last != active:
                active.handle_event("select")

                if last:
                    last.handle_event("deselect")

    def set_members(self, table):
        self.members.table = table
        for sprite in self.members.member_list:
            self.set_member_listeners(sprite)

        self.set_size(*self.size)
        self.set_table_positions()

    def set_member_listeners(self, sprite):
        sprite.add_listener({
            'name': 'change_size',
            'response': {'name': 'change_member_size', 'member': sprite},
            'target': self
        })
        sprite.add_listener({
            'name': 'select',
            'response': {'name': 'option_selected', 'option': sprite},
            'target': self
        })
        sprite.add_listener({
            'name': 'deselect',
            'response': {'name': 'option_deselected', 'option': sprite},
            'target': self
        })
        sprite.add_listener({
            'name': 'activate',
            'response': {'name': 'option_activated', 'option': sprite},
            'target': self
        })

    def set_table_positions(self):
        border_size = 0, 0
        style = self.style
        if "border" in style:
            border_size = self.graphics.border_size

        buffers = style.get("buffers", (0, 0))
        aligns = style.get("aligns", None)

        self.members.set_member_positions(
            self.position, self.size,
            border_size, buffers, aligns
        )

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

    def set_size(self, w, h):
        style = self.style
        w, h = self.members.adjust_size(
            self.size, style["border_size"],
            style["buffers"]
        )
        super(BlockSprite, self).set_size(w, h)

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

    def move(self, dx, dy, v=1):
        super(BlockSprite, self).move(dx, dy, v=v)

        for sprite in self.members.member_list:
            sprite.move(dx, dy, v=v)

    def on_spawn(self):
        super(BlockSprite, self).on_spawn()

        if self.members.active_member:
            self.members.active_member.handle_event("select")

    def on_change_position(self):
        self.set_table_positions()

    def on_change_size(self):
        self.set_table_positions()
        self.graphics.reset_image()

    def on_change_member_size(self):
        self.set_size(*self.size)
        self.set_table_positions()

    def on_pause_pointer(self):
        self.pointer_paused = not self.pointer_paused

    def on_move_pointer(self):
        event = self.event
        x, y = event["value"]
        self.move_pointer(x, y)


class TextSprite(GuiSprite):
    def __init__(self, name):
        super(TextSprite, self).__init__(name)
        self.graphics = TextGraphics(self)
        self.text = ""

    def get_text(self):
        text = self.text
        if not text:
            text = self.name

        return text

    def set_text(self, text):
        self.text = text
        self.handle_event({
            'name': 'change_text',
            'text': text
        })

    def on_change_text(self):
        self.graphics.reset_image()

    def on_select(self):
        self.style = {"font_color": (0, 255, 0)}
        self.set_text(self.text)

    def on_deselect(self):
        self.style = {"font_color": (255, 255, 255)}
        self.set_text(self.text)
