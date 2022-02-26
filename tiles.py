import math
import random

PHI = (1 + math.sqrt(5)) / 2


class Tile:

    # The vertices property is ordered, meaning the vertex's index correlates to a tile vertex.
    # For the dart, going in a clock-wise direction, the point or nose of the dart would be v0.
    # For the kite, imagine it's an actual kite you would fly and you were holding it upright. The kite of the kite is
    # v0 and the rest are followed in a clock-wise direction.
    def __init__(self, name, vertices=None, tile_id=-1):
        self.name = name
        self.vertices = vertices
        self.tile_id = tile_id
        self.color = (random.randint(15, 200), random.randint(15, 255), random.randint(15, 255))
        self.center = None

    def __eq__(self, other):
        if self.name != other.name:
            return False

        value = (self.center[0] - other.center[0]) + (self.center[1] - other.center[1])
        if abs(value) < 0.001:
            return True
        return False

    def initial_shape(self, coordinates, unit_length):
        v0, v1, v2, v3 = coordinates, (0, 0), (0, 0), (0, 0)
        x, y = coordinates

        if self.name == 'dart':
            v1 = ((-1 * PHI * unit_length * rotate(54, 'cos')) + x, (-1 * PHI * unit_length * rotate(54, 'sin')) + y)
            v2 = (x, y - unit_length)
            v3 = ((PHI * unit_length * rotate(54, 'cos')) + x, (-1 * PHI * unit_length * rotate(54, 'sin') + y))
        else:
            v3 = ((unit_length * rotate(18, 'cos')) + x, (-1 * unit_length * rotate(18, 'sin') + y))
            v2 = (x, y - unit_length * PHI)
            v1 = ((-1 * unit_length * rotate(18, 'cos')) + x, (-1 * unit_length * rotate(18, 'sin')) + y)

        # Rotate the tile to match user's orientation
        v0 = self.rotate_point(v0, v0, 0)
        v1 = self.rotate_point(v1, v0, 180)
        v2 = self.rotate_point(v2, v0, 180)
        v3 = self.rotate_point(v3, v0, 180)

        self.vertices = [v0, v1, v2, v3]
        self.round_vertices()
        self.calculate_center()

    def set_random_color(self):
        self.color = (random.randint(10, 255), random.randint(10, 255), random.randint(10, 255))

    def set_color(self, rgb):
        self.color = rgb

    def calculate_center(self):
        x, y = 0, 0
        for vertex in self.vertices:
            x += vertex[0]
            y += vertex[1]
        x /= (len(self.vertices))
        y /= (len(self.vertices))

        self.center = self.round_coordinates((x, y))

    def round_vertices(self, n=6):
        new_vertices = []
        for vertex in self.vertices:
            new_vertices.append(self.round_coordinates(vertex, n))
        self.vertices = new_vertices

    @staticmethod
    def round_coordinates(coordinates, n=6):
        return round(coordinates[0], n), round(coordinates[1], n)

    @staticmethod
    def rotate_point(point_to_rotate, point_of_rotation, degrees_of_rotation):
        precision = 10
        # Convert degrees to radians
        radians = (degrees_of_rotation * math.pi) / 180

        # Math: Translates Cartesian coordinates to polar, rotates, then maps back to Cartesian.
        new_x = point_of_rotation[0] + (point_to_rotate[0] - point_of_rotation[0]) * round(math.cos(radians),
                                                                                           precision) - (
                        point_to_rotate[1] - point_of_rotation[1]) * round(math.sin(radians), precision)

        new_y = point_of_rotation[1] + (point_to_rotate[0] - point_of_rotation[0]) * round(math.sin(radians),
                                                                                           precision) + (
                        point_to_rotate[1] - point_of_rotation[1]) * round(math.cos(radians), precision)

        return round(round(new_x, precision + 4), precision + 2), round(round(new_y, precision + 4), precision + 2)

# ***** The Rounding Problem *****
# The recursive algorithm stops because there is a slight rounding error. When n is large, there is a high chance
# of the algorithm stopping, because the vertices will not match. When n is too small, the tiles do not align properly
# but has a less chance of stopping the recursion.
# The program seems to have minimal breaks when n=2 or n=3.
#
# Truncating the values causes the program to go erratic and place tiles in the wrong direction or not at all. However,
# I do feel that truncating the values may produce a better end result but will require a lot more debugging.
# Furthermore, I have found that when changing the std_len, or the tile's size, the program experiences many more
# rounding errors which causes new tiles to be placed on top of already existing tiles or not placed at all.
# Therefore the optimal values I have found are: n=3 and std_length=50
#
# When I decrease the std_length, I need to increase n. Not exactly sure what the problem is.
# Pairings: (n = 4, std_length = 25), (5, 17), (6, 12)


def rotate(angle, trig_function):
    if trig_function == 'cos':
        return round(math.cos(angle * (math.pi / 180)), 10)
    elif trig_function == 'sin':
        return round(math.sin(angle * (math.pi / 180)), 10)
    else:
        print('trig function ', trig_function, ' not found.')
