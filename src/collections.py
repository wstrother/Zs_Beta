class Group:
    """
    Group is a list subclass with named instances that hold sprite objects
    """
    def __init__(self, name):
        self.name = name
        self.sprites = []

    def __repr__(self):
        n = self.name
        m = len(self.sprites)

        return "Group: {} ({} members)".format(n, m)

    def add_member(self, member):
        if member not in self.sprites:
            self.sprites.append(member)


class CacheList(list):
    def __init__(self, size):
        super(CacheList, self).__init__()
        self._size = size

    def set_size(self):
        if len(self) > self._size:
            for i in range(len(self) - 1):
                self[i] = self[i + 1]
            self.pop()

    def append(self, p_object):
        super(CacheList, self).append(p_object)
        self.set_size()

    def __iadd__(self, other):
        for item in other:
            self.append(item)

        return self


class AverageCache(CacheList):
    def average(self):
        if not self:
            return []

        if type(self[0]) in (int, float):
            return sum(self) / len(self)

        else:
            lhs = [i[0] for i in self]
            rhs = [i[1] for i in self]

            return (sum(lhs) / len(lhs)), (sum(rhs) / len(rhs))


class ChangeCache(CacheList):
    def changes(self, maximum):
        changes = []
        last = None
        for item in self:
            if item != last:
                last = item
                changes.append(item)

        if len(self) > maximum:
            return changes[-maximum:]

        else:
            return changes


