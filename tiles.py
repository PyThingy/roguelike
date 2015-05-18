
import items
from actions import ActionException
from colors import Colors


class Tile:
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.item = None

    def passable(self):
        raise NotImplemented

    def glyph(self):
        raise NotImplemented


class Floor(Tile):
    def passable(self):
        return True

    def glyph(self):
        return self.item.glyph() if self.item else ('.', Colors.DARK_GRAY)

# new comment
class Wall(Tile):
    def passable(self):
        return False

    def glyph(self):
        return ('#', Colors.DARK_GRAY)

    def __str__(self):
        return "wall"


class Door(Tile):
    OPEN = 1
    CLOSED = 2

    def __init__(self, y, x):
        super().__init__(y, x)
        self.item = False
        self.state = Door.CLOSED

    def passable(self):
        return self.state == Door.OPEN

    def glyph(self):
        return ('/' if self.passable() else '+', Colors.BROWN)

    def open(self):
        if self.state == Door.CLOSED:
            self.state = Door.OPEN
        else:
            raise ActionException("it's already open")

    def close(self):
        if self.state == Door.OPEN:
            self.state = Door.CLOSED
        else:
            raise ActionException("it's already closed")

    def __str__(self):
        return "door"


    def use(self, item):
        if isinstance(item, items.Knife):
            return "you stab at the door, leaving a mark"

# new comment
# new comment
class TileFactory:
    TILES = {
        '.': Floor,
        '#': Wall,
        '+': Door,
        '1': Floor,
        '2': Floor,
    }

    @staticmethod
    def make_tile(character, y, x):
        klass = TileFactory.TILES[character]
        return klass(y, x)

