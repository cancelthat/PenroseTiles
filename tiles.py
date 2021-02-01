import math
import random

from tiles_helper_functions import rotate_point

PHI = (1 + math.sqrt(5)) / 2


class Tile:

    def __init__(self, name, vertices=None, tile_id=-1):
        self.name = name
        self.vertices = vertices
        self.color = (random.randint(10, 255), random.randint(10, 255), random.randint(10, 255))
        self.tile_id = tile_id

    def __eq__(self, other):
        precision = 5
        v0 = (round(self.vertices[0][0], precision), round(self.vertices[0][1], precision))
        v1 = (round(self.vertices[1][0], precision), round(self.vertices[1][1], precision))
        v2 = (round(self.vertices[2][0], precision), round(self.vertices[2][1], precision))
        v3 = (round(self.vertices[3][0], precision), round(self.vertices[3][1], precision))

        p0 = (round(other.vertices[0][0], precision), round(other.vertices[0][1], precision))
        p1 = (round(other.vertices[1][0], precision), round(other.vertices[1][1], precision))
        p2 = (round(other.vertices[2][0], precision), round(other.vertices[2][1], precision))
        p3 = (round(other.vertices[3][0], precision), round(other.vertices[3][1], precision))

        return self.name == other.name and v0 == p0 and v1 == p1 and v2 == p2 and v3 == p3

    def initial_shape(self, coordinates, length):
        v0, v1, v2, v3 = coordinates, (0, 0), (0, 0), (0, 0)
        x, y = coordinates
        prec = 10
        if self.name == 'dart':
            v1 = ((PHI * length * -1 * round(math.cos(54 * (math.pi / 180)), prec)) + x,
                  (PHI * length * -1 * round(math.sin(54 * (math.pi / 180)), prec)) + y)
            v2 = (x, y - length)
            v3 = ((PHI * length * round(math.cos(54 * (math.pi / 180)), prec)) + x,
                  (PHI * -1 * length * round(math.sin(54 * (math.pi / 180)), prec)) + y)
        else:
            v3 = ((length * round(math.cos(18 * (math.pi / 180)), prec)) + x,
                  (length * -1 * round(math.sin(18 * (math.pi / 180)), prec)) + y)
            v2 = (x, y - length * PHI)
            v1 = ((length * -1 * round(math.cos(18 * (math.pi / 180)), prec)) + x,
                  (length * -1 * round(math.sin(18 * (math.pi / 180)), prec)) + y)

        # Rotate the tile to match user's orientation
        v0 = rotate_point(v0, v0, 0)
        v1 = rotate_point(v1, v0, 180)
        v2 = rotate_point(v2, v0, 180)
        v3 = rotate_point(v3, v0, 180)

        self.vertices = [v0, v1, v2, v3]

    def set_random_color(self):
        self.color = (random.randint(10, 255), random.randint(10, 255), random.randint(10, 255))

    def draw_kite(self, from_tile, direction):
        p0, p1, p2, p3 = from_tile.vertices
        if from_tile.name == 'kite':
            if direction == 'bottom-right':
                v0 = rotate_point(p0, p2, 72)
                v1 = rotate_point(p1, p2, 72)
                v2 = rotate_point(p2, p2, 0)
                v3 = rotate_point(p1, p1, 0)
            elif direction == 'bottom-left':
                v0 = rotate_point(p0, p2, 288)
                v1 = rotate_point(p3, p3, 0)
                v2 = rotate_point(p2, p2, 0)
                v3 = rotate_point(p3, p2, 288)
            elif direction == 'top-right':
                v0 = rotate_point(p0, p0, 0)
                v1 = rotate_point(p3, p0, 72)
                v2 = rotate_point(p2, p1, 144)
                v3 = rotate_point(p1, p1, 0)
            elif direction == 'top-left':
                v0 = rotate_point(p0, p0, 0)
                v1 = rotate_point(p3, p3, 0)
                v2 = rotate_point(p2, p3, 216)
                v3 = rotate_point(p1, p0, 288)
            else:
                print('there\'s a spelling error')
        else:
            if direction == 'bottom-right':
                v0 = rotate_point(p1, p1, 0)
                v1 = rotate_point(p2, p1, 216)
                v2 = rotate_point(p0, p1, 252)
                v3 = rotate_point(p2, p2, 0)
            elif direction == 'bottom-left':
                v0 = rotate_point(p3, p3, 0)
                v1 = rotate_point(p2, p2, 0)
                v2 = rotate_point(p0, p3, 108)
                v3 = rotate_point(p2, p3, 144)
            elif direction == 'top-right':
                v0 = rotate_point(p2, p0, 252)
                v1 = rotate_point(p0, p1, 72)
                v2 = rotate_point(p1, p1, 0)
                v3 = rotate_point(p0, p0, 0)
            elif direction == 'top-left':
                v0 = rotate_point(p2, p0, 108)
                v1 = rotate_point(p0, p0, 0)
                v2 = rotate_point(p3, p3, 0)
                v3 = rotate_point(p0, p3, 288)
            else:
                print('there\'s a spelling error')

        self.vertices = [v0, v1, v2, v3]

    def draw_dart(self, from_tile, direction):
        p0, p1, p2, p3 = from_tile.vertices
        # Dart to Kite
        if from_tile.name == 'kite':
            if direction == 'bottom-right':
                v0 = rotate_point(p1, p1, 0)
                v1 = rotate_point(p2, p1, 288)
                v2 = rotate_point(p0, p1, 252)
                v3 = rotate_point(p2, p2, 0)
            elif direction == 'bottom-left':
                v0 = rotate_point(p3, p3, 0)
                v1 = rotate_point(p2, p2, 0)
                v2 = rotate_point(p0, p3, 108)
                v3 = rotate_point(p2, p3, 72)
            elif direction == 'top-right':
                v0 = rotate_point(p2, p0, 252)
                v1 = rotate_point(p0, p1, 216)
                v2 = rotate_point(p1, p1, 0)
                v3 = rotate_point(p0, p0, 0)
            elif direction == 'top-left':
                v0 = rotate_point(p2, p0, 108)
                v1 = rotate_point(p0, p0, 0)
                v2 = rotate_point(p3, p3, 0)
                v3 = rotate_point(p0, p3, 144)
            else:
                print('there\'s a spelling error')
        # Dart to Dart
        else:
            if direction == 'top-right' or direction == 'bottom-right':
                v0 = rotate_point(p0, p0, 0)
                v1 = rotate_point(p1, p0, 288)
                v2 = rotate_point(p2, p0, 288)
                v3 = rotate_point(p1, p1, 0)
            elif direction == 'top-left' or direction == 'bottom-left':
                v0 = rotate_point(p0, p0, 0)
                v1 = rotate_point(p3, p3, 0)
                v2 = rotate_point(p2, p0, 72)
                v3 = rotate_point(p3, p0, 72)
            else:
                print('there\'s a spelling error')

        self.vertices = [v0, v1, v2, v3]
