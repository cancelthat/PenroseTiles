import math
import random

from tiles_helper_functions import rotate_point, round_coordinates

PHI = (1 + math.sqrt(5)) / 2


class Tile:

    def __init__(self, name, vertices=None, tile_id=-1):
        self.name = name
        self.vertices = vertices
        self.color = (random.randint(10, 255), random.randint(10, 255), random.randint(10, 255))
        self.tile_id = tile_id

    def __eq__(self, other):
        return self.name == other.name and self.vertices == other.vertices

    def initial_shape(self, coordinates, length):
        v0, v1, v2, v3 = coordinates, (0, 0), (0, 0), (0, 0)
        x, y = coordinates

        if self.name == 'dart':
            v1 = ((PHI * length * -1 * math.cos(54 * (math.pi / 180))) + x,
                  (PHI * length * -1 * math.sin(54 * (math.pi / 180))) + y)
            v2 = (x, y - length)
            v3 = ((PHI * length * math.cos(54 * (math.pi / 180))) + x,
                  (PHI * -1 * length * math.sin(54 * (math.pi / 180))) + y)
        else:
            v3 = ((length * math.cos(18 * (math.pi / 180))) + x,
                  (length * -1 * math.sin(18 * (math.pi / 180))) + y)
            v2 = (x, y - length * PHI)
            v1 = ((length * -1 * math.cos(18 * (math.pi / 180))) + x,
                  (length * -1 * math.sin(18 * (math.pi / 180))) + y)

        # Rotate the tile to match user's orientation
        v1 = rotate_point(v1, v0, 180)
        v2 = rotate_point(v2, v0, 180)
        v3 = rotate_point(v3, v0, 180)

        self.vertices = round_coordinates([v0, v1, v2, v3])

    def set_random_color(self):
        self.color = (random.randint(10, 255), random.randint(10, 255), random.randint(10, 255))

    def draw_kite(self, from_tile, direction):
        p0, p1, p2, p3 = from_tile.vertices
        v0, v1, v2, v3 = p0, p1, p2, p3

        # Kite to Kite
        if from_tile.name == 'kite':
            if direction == 'bottom-right':
                v0 = rotate_point(p0, p2, 72)
                v1 = rotate_point(p1, p2, 72)
                v2 = p2
                v3 = p1
            elif direction == 'bottom-left':
                v0 = rotate_point(p0, p2, 288)
                v1 = p3
                v2 = p2
                v3 = rotate_point(p3, p2, 288)
            elif direction == 'top-right':
                v0 = p0
                v1 = rotate_point(p3, p0, 72)
                v2 = rotate_point(p2, p1, 144)
                v3 = p1
            elif direction == 'top-left':
                v0 = p0
                v1 = p3
                v2 = rotate_point(p2, p3, 216)
                v3 = rotate_point(p1, p0, 288)
            else:
                print('there\'s a spelling error')
        # Kite to Dart
        else:
            if direction == 'bottom-right':
                v0 = p1
                v1 = rotate_point(p2, p1, 216)
                v2 = rotate_point(p0, p1, 252)
                v3 = p2
            elif direction == 'bottom-left':
                v0 = v3
                v1 = p2
                v2 = rotate_point(p0, p3, 108)
                v3 = rotate_point(p2, p3, 144)
            elif direction == 'top-right':
                v0 = rotate_point(p2, p0, 252)
                v1 = rotate_point(p0, p1, 72)
                v2 = p1
                v3 = p0
            elif direction == 'top-left':
                v0 = rotate_point(p2, p0, 108)
                v1 = p0
                v2 = p3
                v3 = rotate_point(p0, p3, 288)
            else:
                print('there\'s a spelling error')

        self.vertices = round_coordinates([v0, v1, v2, v3])

    def draw_dart(self, from_tile, direction):
        p0, p1, p2, p3 = from_tile.vertices
        v0, v1, v2, v3 = (0, 0), (0, 50), (50, 0), (50, 50)

        # Dart to Kite
        if from_tile.name == 'kite':
            if direction == 'bottom-right':
                v0 = p1
                v1 = rotate_point(p2, p1, 288)
                v2 = rotate_point(p0, p1, 252)
                v3 = p2
            elif direction == 'bottom-left':
                v0 = p3
                v1 = p2
                v2 = rotate_point(p0, p3, 108)
                v3 = rotate_point(p2, p3, 72)
            elif direction == 'top-right':
                v0 = rotate_point(p2, p0, 252)
                v1 = rotate_point(p0, p1, 216)
                v2 = p1
                v3 = p0
            elif direction == 'top-left':
                v0 = rotate_point(p2, p0, 108)
                v1 = p0
                v2 = p3
                v3 = rotate_point(p0, p3, 144)
            else:
                print('there\'s a spelling error')
        # Dart to Dart
        else:
            if direction == 'top-right' or direction == 'bottom-right':
                v0 = p0
                v1 = rotate_point(p1, p0, 288)
                v2 = rotate_point(p2, p0, 288)
                v3 = p1
            elif direction == 'top-left' or direction == 'bottom-left':
                v0 = p0
                v1 = p3
                v2 = rotate_point(p2, p0, 72)
                v3 = rotate_point(p3, p0, 72)
            else:
                print('there\'s a spelling error')

        self.vertices = round_coordinates([v0, v1, v2, v3])
