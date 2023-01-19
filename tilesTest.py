import math
import random


class Tile:

    def __init__(self, name):
        self.name = name
        self.vertex_coordinates = []
        self.vertices = []
        self.center = None
        self.color = (random.randint(15, 255), random.randint(15, 255), random.randint(15, 255))

    def initial_shape(self, coordinates, unit_length):
        x, y = coordinates
        s = unit_length
        t = (1 + math.sqrt(5)) / 2
        cos = math.cos(54 * (math.pi / 180))
        sin = math.sin(54 * (math.pi / 180))

        if self.name == 'dart':
            v0 = coordinates
            v1 = (-s * t * cos + x, -s * t * sin + y)
            v2 = (x, y - s)
            v3 = (s * t * cos + x, -s * t * sin + y)
        else:
            v0 = (x, y - s * t)
            v1 = (x + s * t * cos, y - s * t * sin)
            v2 = coordinates
            v3 = (x - s * t * cos, y - s * t * sin)

        self.vertex_coordinates = [v0, v1, v2, v3]
        self.center = ((v0[0] + v1[0] + v2[0] + v3[0]) / 4, (v0[1] + v1[1] + v2[1] + v3[1]) / 4)

    @staticmethod
    def rotate_point(a, b, degrees):  # Rotates point A around point B
        radians = (degrees * math.pi) / 180
        x = b[0] + (a[0] - b[0]) * math.cos(radians) - (a[1] - b[1]) * math.sin(radians)
        y = b[1] + (a[0] - b[0]) * math.sin(radians) + (a[1] - b[1]) * math.cos(radians)
        return x, y
