
# Both Kite and Dart classes are defined here because I needed to reference each of them in the deflate methods

from tiles import Tile


class Kite(Tile):

    def __init__(self):
        super(Kite, self).__init__(name='kite')

    def draw(self, from_tile, direction):
        p0, p1, p2, p3 = from_tile.vertices
        if from_tile.name == 'kite':
            if direction == 'bottom-right':
                v0 = self.rotate_point(p0, p2, 72)
                v1 = self.rotate_point(p1, p2, 72)
                v2 = p2
                v3 = p1
            elif direction == 'bottom-left':
                v0 = self.rotate_point(p0, p2, -72)
                v1 = p3
                v2 = p2
                v3 = self.rotate_point(p3, p2, -72)
            elif direction == 'top-right':
                v0 = p0
                v1 = self.rotate_point(p3, p0, 72)
                v2 = self.rotate_point(p2, p1, 144)
                v3 = p1
            elif direction == 'top-left':
                v0 = p0
                v1 = p3
                v2 = self.rotate_point(p2, p3, -144)
                v3 = self.rotate_point(p1, p0, -72)
            else:
                print('there\'s a spelling error')
        else:
            if direction == 'bottom-right':
                v0 = p1
                v1 = self.rotate_point(p2, p1, -144)
                v2 = self.rotate_point(p0, p1, -108)
                v3 = p2
            elif direction == 'bottom-left':
                v0 = p3
                v1 = p2
                v2 = self.rotate_point(p0, p3, 108)
                v3 = self.rotate_point(p2, p3, 144)
            elif direction == 'top-right':
                v0 = self.rotate_point(p2, p0, -108)
                v1 = self.rotate_point(p0, p1, 72)
                v2 = p1
                v3 = p0
            elif direction == 'top-left':
                v0 = self.rotate_point(p2, p0, 108)
                v1 = p0
                v2 = p3
                v3 = self.rotate_point(p0, p3, -72)
            else:
                print('there\'s a spelling error')

        self.set_vertices([v0, v1, v2, v3])

    def deflate(self):
        kite_right, kite_left = Kite(), Kite()
        dart_right, dart_left = Dart(), Dart()

        k1 = self.vertices[0]
        k2 = self.vertices[1]
        k0 = self.rotate_point(k1, k2, -36)
        k3 = self.rotate_point(k1, k2, -72)

        kite_left.set_vertices([k0, k1, k2, k3])

        kite_right.draw(kite_left, 'top-right')
        dart_left.draw(kite_left, 'top-left')
        dart_right.draw(dart_left, 'top-right')

        return kite_left, kite_right, dart_left, dart_right


class Dart(Tile):

    def __init__(self):
        super(Dart, self).__init__(name='dart')

    def draw(self, adjacent_tile, direction):
        p0, p1, p2, p3 = adjacent_tile.vertices

        if adjacent_tile.name == 'kite':
            if direction == 'bottom-right':
                v0 = p1
                v1 = self.rotate_point(p2, p1, -72)
                v2 = self.rotate_point(p0, p1, -108)
                v3 = p2
            elif direction == 'bottom-left':
                v0 = p3
                v1 = p2
                v2 = self.rotate_point(p0, p3, 108)
                v3 = self.rotate_point(p2, p3, 72)
            elif direction == 'top-right':
                v0 = self.rotate_point(p2, p0, -108)
                v1 = self.rotate_point(p0, p1, -144)
                v2 = p1
                v3 = p0
            elif direction == 'top-left':
                v0 = self.rotate_point(p2, p0, 108)
                v1 = p0
                v2 = p3
                v3 = self.rotate_point(p0, p3, 144)
            else:
                print('there\'s a spelling error')
        else:
            if direction == 'top-right' or direction == 'bottom-right':
                v0 = p0
                v1 = self.rotate_point(p1, p0, -72)
                v2 = self.rotate_point(p2, p0, -72)
                v3 = p1
            elif direction == 'top-left' or direction == 'bottom-left':
                v0 = p0
                v1 = p3
                v2 = self.rotate_point(p2, p0, 72)
                v3 = self.rotate_point(p3, p0, 72)
            else:
                print('there\'s a spelling error')

        self.set_vertices([v0, v1, v2, v3])

    def deflate(self):
        kite_middle = Kite()
        dart_right, dart_left = Dart(), Dart()

        k0 = self.vertices[2]
        k2 = self.vertices[0]
        k1 = self.rotate_point(k0, k2, 36)
        k3 = self.rotate_point(k0, k2, -36)
        kite_middle.set_vertices([k0, k1, k2, k3])

        dart_right.draw(kite_middle, 'top-right')
        dart_left.draw(kite_middle, 'top-left')

        return kite_middle, dart_right, dart_left

