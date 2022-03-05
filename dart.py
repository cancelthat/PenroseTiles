from tiles import Tile


class Dart(Tile):

    def __init__(self):
        super(Dart, self).__init__(name='dart')

    def draw(self, adjacent_tile, direction):
        p0, p1, p2, p3 = adjacent_tile.vertices

        if adjacent_tile.name == 'kite':
            if direction == 'bottom-right':
                v0 = p1
                v1 = self.rotate_point(p2, p1, 36*8)
                v2 = self.rotate_point(p0, p1, 36*7)
                v3 = p2
            elif direction == 'bottom-left':
                v0 = p3
                v1 = p2
                v2 = self.rotate_point(p0, p3, 36*3)
                v3 = self.rotate_point(p2, p3, 36*2)
            elif direction == 'top-right':
                v0 = self.rotate_point(p2, p0, 36*7)
                v1 = self.rotate_point(p0, p1, 36*6)
                v2 = p1
                v3 = p0
            elif direction == 'top-left':
                v0 = self.rotate_point(p2, p0, 36*3)
                v1 = p0
                v2 = p3
                v3 = self.rotate_point(p0, p3, 36*4)
            else:
                print('there\'s a spelling error')
        else:
            if direction == 'top-right' or direction == 'bottom-right':
                v0 = p0
                v1 = self.rotate_point(p1, p0, 36*8)
                v2 = self.rotate_point(p2, p0, 36*8)
                v3 = p1
            elif direction == 'top-left' or direction == 'bottom-left':
                v0 = p0
                v1 = p3
                v2 = self.rotate_point(p2, p0, 36*2)
                v3 = self.rotate_point(p3, p0, 36*2)
            else:
                print('there\'s a spelling error')

        self.vertices = [v0, v1, v2, v3]
        self.round_vertices()
        self.calculate_center()
