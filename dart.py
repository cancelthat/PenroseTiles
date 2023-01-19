from tilesTest import Tile


class Dart(Tile):

    def __init__(self):
        super(Dart, self).__init__(name='dart')

    def draw(self, neighbor, direction):
        p0, p1, p2, p3 = neighbor.vertex_coordinates
        v0 = v1 = v2 = v3 = None
        if neighbor.name == 'kite':
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

        self.vertex_coordinates = [v0, v1, v2, v3]
        self.center = ((v0[0] + v1[0] + v2[0] + v3[0]) / 4, (v0[1] + v1[1] + v2[1] + v3[1]) / 4)
