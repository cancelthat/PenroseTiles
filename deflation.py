from tiles import Tile, rotate_point, round_coordinates
from forced_tiles_recursion_functions import update_dictionary, remove_completed_vertices


def deflate(tiles):
    new_tiles = []
    new_dictionary = {}
    for tile in tiles:
        if tile.name == 'kite':
            eggs = deflate_kite(tile)
            for bacon in eggs:
                new_tiles.append(bacon)
                update_dictionary(new_dictionary, bacon)
        elif tile.name == 'dart':
            eggs = deflate_dart(tile)
            for bacon in eggs:
                new_tiles.append(bacon)
                update_dictionary(new_dictionary, bacon)

    remove_completed_vertices(new_dictionary)
    for val in new_dictionary:
        print(val, len(new_dictionary[val]))
        vertices = []
        for vertex in new_dictionary[val]:
            vertices.append(vertex[0].vertices)
        print(vertices)

    return new_tiles, new_dictionary


def deflate_kite(tile):
    v0, v1, v2, v3 = tile.vertices
    left_kite, right_kite = Tile('kite'), Tile('kite')
    left_dart, right_dart = Tile('dart'), Tile('dart')

    left_kite.vertices = round_coordinates([rotate_point(v0, v1, 324),
                                            v0,
                                            v1,
                                            rotate_point(v0, v1, 288)])

    right_kite.vertices = round_coordinates([rotate_point(v0, v3, 36),
                                             rotate_point(v0, v3, 72),
                                             v3,
                                             v0])

    left_dart.vertices = round_coordinates([v2,
                                            rotate_point(v0, v1, 324),
                                            rotate_point(v0, v1, 288),
                                            rotate_point(v0, v1, 252)])

    right_dart.vertices = round_coordinates([v2,
                                             rotate_point(v0, v3, 108),
                                             rotate_point(v0, v3, 72),
                                             rotate_point(v0, v3, 36)])

    return [left_kite, right_kite, left_dart, right_dart]


def deflate_dart(tile):
    v0, v1, v2, v3 = tile.vertices
    new_kite, = Tile('kite'),
    left_dart, right_dart = Tile('dart'), Tile('dart')

    new_kite.vertices = round_coordinates([v2,
                                           rotate_point(v2, v0, 36),
                                           v0,
                                           rotate_point(v2, v0, 324)])

    left_dart.vertices = round_coordinates([v1,
                                            v2,
                                            rotate_point(v2, v0, 324),
                                            rotate_point(v2, v0, 288)])

    right_dart.vertices = round_coordinates([v3,
                                             rotate_point(v2, v0, 72),
                                             rotate_point(v2, v0, 36),
                                             v2])

    return [new_kite, left_dart, right_dart]
