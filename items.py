from colors import Colors


class Item:
    def glyph(self):
        raise NotImplemented

    def __str__(self):
        raise NotImplemented


class Knife(Item):
    def glyph(self):
        return ('(', Colors.YELLOW)

    def __str__(self):
        return "knife"


class Key(Item):
    def glyph(self):
        return('K', Colors.DARK_RED)

    def __str__(self):
        return "key"

class Pickaxe(Item):
    def __init__(self):
        self.usage = 3

    def glyph(self):
        return ('P', Colors.DARK_GRAY) if self.usage < 1 else ('P', Colors.BROWN)

    def pickaxe_used(self):
        self.usage -= 1

    def get_pickaxe_usage(self):
        return self.usage

    def __str__(self):
        return "pickaxe (%s)" % self.usage