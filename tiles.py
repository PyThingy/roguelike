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

    # powinno byc jeszcze use(...), walk() etc.


class Floor(Tile):
    def passable(self):
        return True

    def glyph(self):
        return self.item.glyph() if self.item else ('.', Colors.DARK_GRAY)


class KeyFloor(Floor):
    def __init__(self, y, x):
        super().__init__(y,x)
        self.item = Key()


class KnifeFloor(Floor):
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.item = items.Knife()


class Wall(Tile):
    def __init__(self,y,x):
        self.y = y
        self.x = x
        self.destroyed = False

    def passable(self):
        if self.destroyed:
            return True
        else:
            return False

    def glyph(self):
        return ('#', Colors.DARK_GRAY) if self.destroyed else ('#', Colors.WHITE)

    def __str__(self):
        return "wall"

    def use(self, item):
        if isinstance(item, items.Pickaxe) and item.get_pickaxe_usage() > 0:
            self.destroyed = True
            item.pickaxe_used()
            return "you have destroyed the wall, %s" % item
        else:
            raise ActionException("You can not use %s here" % item)


class Teleport(Tile):
    def passable(self):
        return True

    def glyph(self):
        return ('T', Colors.DARK_RED)

    def __str__(self):
        return "teleport"

    def open(self):
        return "you used the teleport"


class Door(Tile):
    OPEN = 1
    CLOSED = 2

    def __init__(self, y, x):
        super().__init__(y, x)
        self.item = False
        self.state = Door.CLOSED
        self.destroyed = False

    def passable(self):
        return True if self.destroyed or self.state == Door.OPEN else False

    def glyph(self):
        return (';', Colors.DARK_GRAY) if self.destroyed else ('/' if self.passable() else '+', Colors.BROWN)

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
        if not self.destroyed:
            if isinstance(item, items.Knife):
                return "you stab at the door, leaving a mark"
            if isinstance(item, items.Pickaxe) and item.get_pickaxe_usage() > 0:
                    self.destroyed = True
                    item.pickaxe_used()
                    return "you have destroyed the door, %s" % item


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
        self.destroyed = False

    def glyph(self):
        return (';', Colors.DARK_GRAY) if self.destroyed else (self.glyphs[self.state], Colors.DARK_RED)

    def open(self):
        if not self.destroyed:
            if self.state == KeyDoor.LOCKED:
                raise ActionException("this door is locked")
            super().open()

    def use(self, item):
        if not self.destroyed:
            if isinstance(item, items.Pickaxe) and item.get_pickaxe_usage() > 0:
                self.destroyed = True
                item.pickaxe_used()
                return "you have destroyed the door, %s" % item
            if isinstance(item, items.Key) and self.state == KeyDoor.LOCKED:
                self.state = KeyDoor.CLOSED
                return "you have unlocked the door"
            if isinstance(item, items.Key) and self.state == KeyDoor.CLOSED:
                self.state = KeyDoor.LOCKED
                return "you have locked the door"
            else:
                raise ActionException("Close the door, please.")
            super().use(item)


class PickaxeFloor(Floor):
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.item = items.Pickaxe()


class TileFactory:
    TILES = {
        '.': Floor,
        '#': Wall,
        '+': Door,
        '1': KeyDoor,
        '2': KeyFloor,
        '3': Teleport,
        '(': KnifeFloor,
        'P': PickaxeFloor,
    }

    @staticmethod
    def make_tile(character, y, x):
        klass = TileFactory.TILES[character]
        return klass(y, x)
