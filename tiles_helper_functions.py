import math
import numpy as np


# ***** The Rounding Problem *****
# The recursive algorithm stops because there is a slight rounding error. When n is large, there is a high chance
# of the algorithm stopping, because the vertices will not match. When n is too small, the tiles do not align properly
# but has a less chance of stopping the recursion.
# The program seems to have minimal breaks when n=2 or n=3.
#
# Truncating the values causes the program to go erratic and place tiles in the wrong direction or not at all. However,
# I do feel that truncating the values may produce a better end result but will require a lot of debugging.
# Furthermore, I have found that changing the std_len, or the tile's size, the program experiences many more rounding
# errors which causes new tiles to be placed on top of already existing tiles or not placed at all.
# Therefore the optimal values I have found are: n=3 and std_length=50
#
# When I decrease the std_length, I need to increase n.

def round_coordinates(coordinates, n=4):
    rounded = []
    for val in coordinates:
        rounded.append((round(val[0], n), round(val[1], n)))
    return rounded


def rotate_point(point_to_rotate, point_of_rotation, degrees_of_rotation):
    # Convert degrees to radians
    radians = (degrees_of_rotation * math.pi) / 180

    # Math: Translates Cartesian coordinates to polar, rotates, then maps back to Cartesian.
    new_X = point_of_rotation[0] + (point_to_rotate[0] - point_of_rotation[0]) * math.cos(radians) - (
            point_to_rotate[1] - point_of_rotation[1]) * math.sin(radians)

    new_Y = point_of_rotation[1] + (point_to_rotate[0] - point_of_rotation[0]) * math.sin(radians) + (
            point_to_rotate[1] - point_of_rotation[1]) * math.cos(radians)

    return new_X, new_Y


def truncate_coordinates(coordinates, n=4):
    return_list = []
    for val in coordinates:
        return_list.append((truncate(val[0], n), truncate(val[1], n)))
    return return_list


def truncate(value, n):
    x = 10.0 ** n
    return math.trunc(x * value) / x
