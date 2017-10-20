from src.entities import Sprite
from app.sprites.text_sprite import TextSprite


class MemberTable:
    def __init__(self):
        self.table = [[]]
        self.pointer = 0, 0

    @property
    def active_member(self):
        return self.get_member(*self.pointer)

    @property
    def member_list(self):
        l = []
        for row in self.table:
            for item in row:
                l.append(item)

        return l

    def get_member(self, i, j):
        return self.table[i][j]

    def can_select(self, i, j):
        try:
            return self.get_member(i, j) is not None
        except IndexError:
            return False

    def move_pointer(self, x, y):
        i, j = self.pointer
        table = self.table
        start = [i, j]

        cycling = True
        while cycling:
            if x != 0:
                j += x
                cells = len(table[i]) - 1

                if j > cells:
                    j = 0
                elif j < 0:
                    j = cells

            if y != 0:
                i += y
                rows = len(table) - 1

                if i > rows:
                    i = 0
                elif i < 0:
                    i = rows

            self.pointer = [i, j]
            cycling = not self.can_select(*self.pointer)

            if self.pointer == start:
                cycling = False


class BlockSprite(Sprite):
    def __init__(self, name):
        super(BlockSprite, self).__init__(name)
        self.members = MemberTable()

    def set_members(self, table):
        new_table = []
        for key in sorted(table.keys()):
            new_row = []

            for item in table[key]:
                new_row.append(item)

            new_table.append(new_row)

        self.get_sprites_from_table(new_table)

    def get_members(self):
        return self.members.member_list

    def set_group(self, group):
        super(BlockSprite, self).set_group(group)

        for sprite in self.get_members():
            sprite.set_group(group)

    def get_sprites_from_table(self, table):
        new_table = []
        y = 0
        for row in table:
            x = 0
            new_row = []
            for item in row:
                ts = TextSprite(str(item))
                ts.set_text(str(item))
                ts.set_position(x, y)
                new_row.append(ts)

                x += 100
            y += 100
            new_table.append(new_row)

        self.members.table = new_table
