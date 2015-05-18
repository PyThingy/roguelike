import items
from actions import ActionException
from colors import Colors
from actions import ActionException
from items import Key

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


class KeyFloor(Floor):
    def __init__(self, y, x):
        super().__init__(y,x)
        self.item = Key()


class Wall(Tile):
    def passable(self):
        return False

    def glyph(self):
        return ('#', Colors.WHITE)

    def __str__(self):
        return "wall"

class Teleport(Tile):
    def passable(self):
        return True

    def glyph(self):
        return ('T', Colors.DARK_RED)

    def __str__(self):
        return "teleport"

    def open(self):
        return "you used the teleport"


# new comment
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

class KeyDoor(Door):
    LOCKED = 3
    def __init__(self, y, x):
        super().__init__(y,x)
        self.state = KeyDoor.LOCKED

    def glyph(self):
        return('/' if self.passable() else 'D', Colors.YELLOW)

    #def open(self):
    #     if self.state == KeyDoor.OPEN:
    #         self.state = KeyDoor.CLOSED
    #     else:
    #         raise ActionException("do you have a key?")

    def use(self, item):
        if isinstance(item, Key):
            self.state = KeyDoor.CLOSED
            return "you opended the door"


class TileFactory:
    TILES = {
        '.': Floor,
        '#': Wall,
        '+': Door,
        '1': KeyDoor,
        '2': KeyFloor,
        '3': Teleport,
    }

    @staticmethod
    def make_tile(character, y, x):
        klass = TileFactory.TILES[character]
        return klass(y, x)

