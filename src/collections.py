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
