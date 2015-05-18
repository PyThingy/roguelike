# to do:
# patrzenie na sciany
# spacerujace kozy :D
# pijane kozy
# i cokolwiek tylko wymy�limy
# (zachowajmy to dla siebie, bedziemy mergowac razem za tydzien)

import items
from actions import ActionException
from colors import Colors
from actions import ActionException


class Tile:
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.item = None

    def passable(self):
        raise NotImplemented

    def glyph(self):
        raise NotImplemented
    
    # powinno byc jeszcze use(...), walk() etc.


class Floor(Tile):
    def passable(self):
        return True

    def glyph(self):
        return self.item.glyph() if self.item else ('.', Colors.DARK_GRAY)

# new comment

class KeyFloor(Floor):
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.item = items.Key() # Key() - instancja; Key - cala klasa!

class KnifeFloor(Floor):
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.item = items.Knife()


class KeyFloor(Floor):
    def __init__(self,y,x):
        super().__init__(y,x)
        self.item = items.Key()


class Wall(Tile):
    def passable(self):
        return False

    def glyph(self):
        return ('#', Colors.DARK_GRAY)

    def __str__(self):
        return "wall"

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
    glyphs = {
        1: '/',
        2: '+',
        3: '|',
    }

    def __init__(self, y, x):
        super().__init__(y, x)
        self.state = KeyDoor.LOCKED

    def glyph(self):
        return (self.glyphs[self.state], Colors.DARK_RED)

    def open(self):
        if self.state == KeyDoor.LOCKED:
            raise ActionException("this door is locked")
        super().open()

    def use(self, item):
        if isinstance(item, items.Key) and self.state == KeyDoor.LOCKED:
            self.state = KeyDoor.CLOSED
            return "you have unlocked the door"
        if isinstance(item, items.Key) and self.state == KeyDoor.CLOSED:
            self.state = KeyDoor.LOCKED
            return "you have locked the door"
        else:
            raise ActionException("Close the door, please.")
        
        super().use(item)


class TileFactory:
    TILES = {
        '.': Floor,
        '#': Wall,
        '+': Door,
        '1': KeyDoor,
        '2': KeyFloor,
        '(': KnifeFloor
    }

    @staticmethod
    def make_tile(character, y, x):
        klass = TileFactory.TILES[character]
        return klass(y, x)
