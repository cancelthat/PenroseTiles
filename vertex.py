from kite import Kite
from dart import Dart


class Vertex:
    def __init__(self, tile_to_add, coordinates, name='edge'):
        self.tiles = [tile_to_add]
        self.coordinates = coordinates
        self.name = name

        # list of 2D tuples, holding a tile and the tile's congruent vertex. ex [(Kite(), 1), (Dart(), 0)]
        self.congruent_vertices = []
        for i, v0 in enumerate(tile_to_add.vertices):
            if v0 == coordinates:
                self.congruent_vertices.append((tile_to_add, i))

    def __eq__(self, other):
        a = self.coordinates
        b = other.coordinates
        value = (a[0]/b[0]) * (a[1]/b[1])
        if 0.99 < value < 1.01:
            return True
        return False

    def add_tile(self, tile_to_add):
        if not (tile_to_add in self.tiles):
            self.tiles.append(tile_to_add)


class Ace(Vertex):
    def __init__(self):
        super(Ace, self).__init__()
        self.name = 'ace'

    def draw(self, dart):
        right_kite = Kite()
        right_kite.draw_kite(dart, 'bottom-left')
        if not False:
            self.tiles.append(right_kite)

        left_kite = Kite()
        left_kite.draw_kite(dart, 'bottom-right')
        self.tiles.append(left_kite)

