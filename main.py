import pygame
import math
from tiles import Tile

# Global Constants
PHI = (1 + math.sqrt(5)) / 2
STD_LEN = 25

# Initializer
pygame.init()

# Display
screenX = 800
screenY = 600
screen = pygame.display.set_mode((screenX, screenY))

# Icon
pygame.display.set_caption('Penrose Tiles')
icon = pygame.image.load('pentagon.png')
pygame.display.set_icon(icon)

# Tile Movement
tile_X_change = 0
tile_Y_change = 0

# Switches
game_is_running = True
kite_is_selected = True

# Pregame Initializations
initial_shape = Tile(name='kite', tile_id=0)
initial_shape.initial_shape((screenX/2, round(screenY / 2 - STD_LEN * PHI, 4)), length=STD_LEN)

# Information Holders
all_tiles = [initial_shape]
vertex_dictionary = {}  # { vertex: (Tile, vertex_index) }


def distance_formula(val1, val2):
    return math.sqrt(pow(val1[0] - val2[0], 2) + pow(val1[1] - val2[1], 2))


def distance_from_tile_to_point(tile, point):
    v0, v1, v2, v3 = tile.vertices
    return distance_formula(v0, point) + distance_formula(v1, point) + distance_formula(v2, point) + distance_formula(v3, point)


def find_closest_tile(tiles, point):
    shortest_distance = math.inf
    closest_tile = None
    for t in tiles:
        dist = distance_from_tile_to_point(t, point)
        if dist < shortest_distance:
            shortest_distance = dist
            closest_tile = t
    return closest_tile


def find_closest_vertex(tile, point):
    v0, v1, v2, v3 = tile.vertices

    vertical = 'top'
    horizontal = 'right'
    if distance_formula(v1, point) >= distance_formula(v3, point):
        horizontal = 'left'
    if distance_formula(v0, point) >= distance_formula(v2, point):
        vertical = 'bottom'
    return vertical + '-' + horizontal


def create_new_tile(tiles):
    mouse = pygame.mouse.get_pos()
    closest_tile = find_closest_tile(tiles, mouse)
    direction = find_closest_vertex(closest_tile, mouse)

    tile_new = Tile(name='kite', tile_id=len(tiles))

    if kite_is_selected:
        tile_new.draw_kite(closest_tile, direction=direction)
    else:
        tile_new.name = 'dart'
        tile_new.draw_dart(closest_tile, direction=direction)

    # Check if a tile exists with matching vertices
    if any(other_tile.vertices == tile_new.vertices for other_tile in tiles):
        return None
    return tile_new


def update_dictionary(dictionary, list_of_all_tiles):
    for tile in list_of_all_tiles:
        for index, vertex in enumerate(tile.vertices):
            if dictionary.get(vertex) is None:
                dictionary[vertex] = [(tile, index)]
            else:
                if not (any(other_tiles == (tile, index) for other_tiles in dictionary[vertex])):
                    dictionary[vertex].append((tile, index))


def check_if_tile_exists(tile, list_of_all_tiles):
    return any(other_tile.vertices == tile.vertices for other_tile in list_of_all_tiles)


def sparse_vertex_dictionary_value(value):
    tiles, indices = [], []

    for item in value:
        tiles.append(item[0])
        indices.append(item[1])
    return tiles, indices


def ace(key, dictionary_value, list_of_all_tiles, dictionary):
    if len(dictionary_value) == 2:
        tiles, indices = sparse_vertex_dictionary_value(dictionary_value)
        left = [('dart', 2), ('kite', 1)]
        right = [('dart', 2), ('kite', 3)]
        vertex = []
        kite_tile = None
        for i in range(len(tiles)):
            vertex.append((tiles[i].name, indices[i]))
            if tiles[i].name == 'kite':
                kite_tile = tiles[i]

        new_kite = Tile('kite')
        if sorted(left) == sorted(vertex):
            new_kite.draw_kite(kite_tile, 'bottom-right')
            list_of_all_tiles.append(new_kite)
            dictionary[key].append((new_kite, 3))
            print('drawing ace...')

        elif sorted(right) == sorted(vertex):
            new_kite.draw_kite(kite_tile, 'bottom-left')
            list_of_all_tiles.append(new_kite)
            dictionary[key].append((new_kite, 1))
            print('drawing ace...')


def sun(key, dictionary_value, list_of_all_tiles, dictionary):
    if 3 <= len(dictionary_value) < 5:
        tiles, indices = sparse_vertex_dictionary_value(dictionary_value)
        for i in range(len(tiles)):
            if not (tiles[i].name == 'kite' and indices[i] == 2):
                return

        new_tile = Tile('kite')
        for tile in tiles:
            new_tile.draw_kite(tile, direction='bottom-right')
            if not check_if_tile_exists(new_tile, list_of_all_tiles):
                # Add tile to list
                list_of_all_tiles.append(new_tile)
                # Update the dictionary
                dictionary[key].append((new_tile, 2))
                # Call again if needed
                if len(tiles) == 3:
                    sun(key, dictionary_value, list_of_all_tiles, dictionary)
                # Exit loop if 5th kite is added
                print('drawing sun...')
                break

            # Check the left side
            new_tile.draw_kite(tiles[i], direction='bottom-left')
            if not check_if_tile_exists(new_tile, list_of_all_tiles):
                list_of_all_tiles.append(new_tile)
                dictionary[key].append((new_tile, 2))
                if len(tiles) == 3:
                    sun(key, dictionary_value, list_of_all_tiles, dictionary)
                print('drawing sun...')

        # Uncomment to color vertex
        # for value in dictionary[key]:
        #    value[0].set_color((30, 145, 203))


def star(key, dictionary_value, list_of_all_tiles, dictionary):
    if len(dictionary_value) == 4:
        tiles, indices = sparse_vertex_dictionary_value(dictionary_value)
        for i in range(len(tiles)):
            if not (tiles[i].name == 'dart' and indices[i] == 0):
                return

        new_tile = Tile('dart')
        for tile in tiles:
            new_tile.draw_dart(tile, direction='bottom-right')
            if not check_if_tile_exists(new_tile, list_of_all_tiles):
                # Add tile to list
                list_of_all_tiles.append(new_tile)
                # Update the dictionary
                dictionary[key].append((new_tile, 0))
                # Exit loop if 5th dart is added
                print('drawing star...')
                break

            # Check the left side
            new_tile.draw_dart(tiles[i], direction='bottom-left')
            if not check_if_tile_exists(new_tile, list_of_all_tiles):
                list_of_all_tiles.append(new_tile)
                dictionary[key].append((new_tile, 0))
                print('drawing star...')

        # Uncomment to color vertex
        # for value in dictionary[key]:
        #    value[0].set_color((250, 234, 44))


def deuce(key, dictionary_value, list_of_all_tiles, dictionary):
    if len(dictionary_value) == 2:
        tiles, indices = sparse_vertex_dictionary_value(dictionary_value)
        for i in range(len(tiles)):
            if not (tiles[i].name == 'kite' and indices[i] == 0):
                return

        if tiles[0].vertices[1] == tiles[1].vertices[3]:
            left_dart = Tile('dart')
            right_dart = Tile('dart')

            left_dart.draw_dart(tiles[0], 'top-left')
            if not check_if_tile_exists(left_dart, list_of_all_tiles):
                list_of_all_tiles.append(left_dart)
                dictionary[key].append((left_dart, 1))

            right_dart.draw_dart(tiles[1], 'top-right')
            if not check_if_tile_exists(right_dart, list_of_all_tiles):
                list_of_all_tiles.append(right_dart)
                dictionary[key].append((right_dart, 3))
            print('drawing deuce...')
            return
        elif tiles[0].vertices[3] == tiles[1].vertices[1]:
            left_dart = Tile('dart')
            right_dart = Tile('dart')

            left_dart.draw_dart(tiles[1], 'top-left')
            if not check_if_tile_exists(left_dart, list_of_all_tiles):
                list_of_all_tiles.append(left_dart)
                dictionary[key].append((left_dart, 1))

            right_dart.draw_dart(tiles[0], 'top-right')
            if not check_if_tile_exists(right_dart, list_of_all_tiles):
                list_of_all_tiles.append(right_dart)
                dictionary[key].append((right_dart, 3))
            print('drawing deuce...')
            return
    elif len(dictionary_value) == 3:
        tiles, indices = sparse_vertex_dictionary_value(dictionary_value)
        left_dart = [('kite', 0), ('kite', 0), ('dart', 1)]
        right_dart = [('kite', 0), ('kite', 0), ('dart', 3)]
        some_kite = [('dart', 1), ('dart', 3), ('kite', 0)]

        vertex = []
        dart_tile = None
        for i in range(len(tiles)):
            vertex.append((tiles[i].name, indices[i]))
            if tiles[i].name == 'dart':
                dart_tile = tiles[i]

        new_tile = Tile('dart')
        if sorted(left_dart) == sorted(vertex):
            new_tile.draw_dart(dart_tile, 'top-right')
            list_of_all_tiles.append(new_tile)
            dictionary[key].append((dart_tile, 3))
            print('drawing deuce...')
            return
        elif sorted(right_dart) == sorted(vertex):
            new_tile.draw_dart(dart_tile, 'top-left')
            list_of_all_tiles.append(new_tile)
            dictionary[key].append((dart_tile, 1))
            print('drawing deuce...')
            return
        elif sorted(some_kite) == sorted(vertex):
            new_tile.name = 'kite'
            for val in dictionary_value:
                if val[0].name == 'dart' and val[1] == 1:
                    new_tile.draw_kite(val[0], 'bottom-right')
                    if not check_if_tile_exists(new_tile, list_of_all_tiles):
                        list_of_all_tiles.append(new_tile)
                        dictionary[key].append((new_tile, 0))
                        print('drawing deuce...')
                        return
                if val[0].name == 'dart' and val[1] == 3:
                    new_tile.draw_kite(val[0], 'bottom-left')
                    if not check_if_tile_exists(new_tile, list_of_all_tiles):
                        list_of_all_tiles.append(new_tile)
                        dictionary[key].append((new_tile, 0))
                        print('drawing deuce...')
                        return


def jack(key, dictionary_value, list_of_all_tiles, dictionary):
    if 2 <= len(dictionary_value) < 5:
        tiles, indices = sparse_vertex_dictionary_value(dictionary_value)
        # Create a list of darts
        darts = []
        vertex = []
        for value in dictionary_value:
            vertex.append((value[0].name, value[1]))
            if value[0].name == 'dart':
                darts.append(value)

        if not darts:
            return
            # code below has not been tested and may not be needed
            # noinspection PyUnreachableCode
            if ('kite', 2) in vertex and ('kite', 0) in vertex:

                # Not really sure how to trigger this case, so it may or may not be working.
                print('!!! Super Duper Special Case Activated !!!')

                top_tile, bottom_tile = None, None
                for i in range(len(tiles)):
                    if indices[i] == 2:
                        top_tile = tiles[i]
                    if indices[i] == 0:
                        bottom_tile = tiles[i]

                # check if v0 of the top kite, is closer to the v1 or v3 of the bottom kite
                v1_dist = distance_formula(top_tile.vertices[0], bottom_tile.vertices[1])
                v3_dist = distance_formula(top_tile.vertices[0], bottom_tile.vertices[3])

                if v1_dist <= v3_dist:
                    top_kite = Tile('kite')
                    right_dart = Tile('dart')
                    left_dart = Tile('dart')

                    top_kite.draw_kite(top_tile, 'bottom-left')
                    if not check_if_tile_exists(top_kite, list_of_all_tiles):
                        list_of_all_tiles.append(top_kite)
                        dictionary[key].append((top_kite, 2))

                    right_dart.draw_kite(bottom_tile, 'top-right')
                    if not check_if_tile_exists(right_dart, list_of_all_tiles):
                        list_of_all_tiles.append(right_dart)
                        dictionary[key].append((right_dart, 3))

                    left_dart.draw_kite(bottom_tile, 'top-left')
                    if not check_if_tile_exists(left_dart, list_of_all_tiles):
                        list_of_all_tiles.append(left_dart)
                        dictionary[key].append((left_dart, 1))
                    return
                else:
                    top_kite = Tile('kite')
                    right_dart = Tile('dart')
                    left_dart = Tile('dart')

                    top_kite.draw_kite(top_tile, 'bottom-right')
                    if not check_if_tile_exists(top_kite, list_of_all_tiles):
                        list_of_all_tiles.append(top_kite)
                        dictionary[key].append((top_kite, 2))

                    right_dart.draw_kite(bottom_tile, 'top-right')
                    if not check_if_tile_exists(right_dart, list_of_all_tiles):
                        list_of_all_tiles.append(right_dart)
                        dictionary[key].append((right_dart, 3))

                    left_dart.draw_kite(bottom_tile, 'top-left')
                    if not check_if_tile_exists(left_dart, list_of_all_tiles):
                        list_of_all_tiles.append(left_dart)
                        dictionary[key].append((left_dart, 1))
                    return

        if len(darts) == 2:
            top_left_kite = Tile('kite')
            top_right_kite = Tile('kite')
            bottom_kite = Tile('kite')
            if darts[0][0].vertices[0] == darts[1][0].vertices[0]:
                return
            if (darts[0][0].vertices[1] == darts[1][0].vertices[3]) or (darts[0][0].vertices[3] == darts[1][0].vertices[1]):

                if darts[0][1] == 1:
                    top_left_kite.draw_kite(darts[0][0], direction='top-right')
                    if not check_if_tile_exists(top_left_kite, list_of_all_tiles):
                        list_of_all_tiles.append(top_left_kite)
                        dictionary[key].append((top_left_kite, 2))

                    top_right_kite.draw_kite(top_left_kite, direction='bottom-right')
                    if not check_if_tile_exists(top_right_kite, list_of_all_tiles):
                        list_of_all_tiles.append(top_right_kite)
                        dictionary[key].append((top_right_kite, 2))

                    bottom_kite.draw_kite(darts[0][0], direction='bottom-right')
                    if not check_if_tile_exists(bottom_kite, list_of_all_tiles):
                        list_of_all_tiles.append(bottom_kite)
                        dictionary[key].append((bottom_kite, 0))
                else:
                    top_right_kite.draw_kite(darts[0][0], direction='top-left')
                    if not check_if_tile_exists(top_right_kite, list_of_all_tiles):
                        list_of_all_tiles.append(top_right_kite)
                        dictionary[key].append((top_right_kite, 2))

                    top_left_kite.draw_kite(top_right_kite, direction='bottom-left')
                    if not check_if_tile_exists(top_left_kite, list_of_all_tiles):
                        list_of_all_tiles.append(top_left_kite)
                        dictionary[key].append((top_left_kite, 2))

                    bottom_kite.draw_kite(darts[0][0], direction='bottom-left')
                    if not check_if_tile_exists(bottom_kite, list_of_all_tiles):
                        list_of_all_tiles.append(bottom_kite)
                        dictionary[key].append((bottom_kite, 0))
                print('drawing jack...')
            return

        if len(darts) == 1:

            if darts[0][1] == 1:
                for value in dictionary_value:
                    if darts[0][0].vertices[0] == value[0].vertices[3]:
                        top_kite = Tile('kite')
                        other_dart = Tile('dart')
                        bottom_kite = Tile('kite')

                        top_kite.draw_kite(value[0], 'bottom-right')
                        if not check_if_tile_exists(top_kite, list_of_all_tiles):
                            list_of_all_tiles.append(top_kite)
                            dictionary[key].append((top_kite, 2))

                        other_dart.draw_dart(top_kite, 'bottom-right')
                        if not check_if_tile_exists(other_dart, list_of_all_tiles):
                            list_of_all_tiles.append(other_dart)
                            dictionary[key].append((other_dart, 3))

                        bottom_kite.draw_kite(darts[0][0], 'bottom-right')
                        if not check_if_tile_exists(bottom_kite, list_of_all_tiles):
                            list_of_all_tiles.append(bottom_kite)
                            dictionary[key].append((bottom_kite, 0))
                        print('drawing jack...')
                        return
            elif darts[0][1] == 3:
                for value in dictionary_value:
                    if darts[0][0].vertices[0] == value[0].vertices[1]:
                        top_kite = Tile('kite')
                        other_dart = Tile('dart')
                        bottom_kite = Tile('kite')

                        top_kite.draw_kite(value[0], 'bottom-left')
                        if not check_if_tile_exists(top_kite, list_of_all_tiles):
                            list_of_all_tiles.append(top_kite)
                            dictionary[key].append((top_kite, 2))

                        other_dart.draw_dart(top_kite, 'bottom-left')
                        if not check_if_tile_exists(other_dart, list_of_all_tiles):
                            list_of_all_tiles.append(other_dart)
                            dictionary[key].append((other_dart, 1))

                        bottom_kite.draw_kite(darts[0][0], 'bottom-left')
                        if not check_if_tile_exists(bottom_kite, list_of_all_tiles):
                            list_of_all_tiles.append(bottom_kite)
                            dictionary[key].append((bottom_kite, 0))
                        print('drawing jack...')
                        return


def prince(key, dictionary_value, list_of_all_tiles, dictionary):
    # A prince vertex has forced tiles, but is only partially completed. It consists of 1 dart and 2 kites.
    # Depending on which tile is placed next, the prince vertex will either become a King vertex or a Queen vertex.

    if len(dictionary_value) == 2:
        tiles, indices = sparse_vertex_dictionary_value(dictionary_value)
        dart, kite = None, None
        for value in dictionary_value:
            if value[0].name == 'kite' and (value[1] == 1 or value[1] == 3):
                kite = value
            if value[0].name == 'dart' and value[1] == 0:
                dart = value

        if dart is None or kite is None:
            return

        new_kite = Tile('kite')
        if kite[0].vertices[2] == dart[0].vertices[3] and kite[0].vertices[1] == dart[0].vertices[0]:
            new_kite.draw_kite(kite[0], 'top-right')
            if not check_if_tile_exists(new_kite, list_of_all_tiles):
                list_of_all_tiles.append(new_kite)
                dictionary[key].append((new_kite, 3))
            return
        if kite[0].vertices[2] == dart[0].vertices[1] and kite[0].vertices[3] == dart[0].vertices[0]:
            new_kite.draw_kite(kite[0], 'top-left')
            if not check_if_tile_exists(new_kite, list_of_all_tiles):
                list_of_all_tiles.append(new_kite)
                dictionary[key].append((new_kite, 1))
            return


def queen(key, dictionary_value, list_of_all_tiles, dictionary):
    if 2 <= len(dictionary_value) < 5:
        tiles, indices = sparse_vertex_dictionary_value(dictionary_value)
        darts = []
        kites = []
        vertex = []
        for i in range(len(tiles)):
            vertex.append((tiles[i].name, indices[i]))
            if tiles[i].name == 'dart':
                darts.append((tiles[i], indices[i]))
            if tiles[i].name == 'kite':
                kites.append((tiles[i], indices[i]))

        if (len(darts) == 1 and darts[0][1] == 0) and (('kite', 1) in vertex and ('kite', 3) in vertex):
            if len(kites) == 2:
                # A single dart with 2 kites to its top-left and top-right
                left_kite, right_kite = None, None
                for kite in kites:
                    if kite[1] == 1 and kite[0].vertices[2] == darts[0][0].vertices[3]:
                        left_kite = kite[0]
                    elif kite[1] == 3 and kite[0].vertices[2] == darts[0][0].vertices[1]:
                        right_kite = kite[0]

                if left_kite is None or right_kite is None:
                    return

                for i in range(len(tiles)):
                    new_left_kite = Tile('kite')
                    new_right_kite = Tile('kite')
                    if (tiles[i].name == 'kite' and indices[i] == 1) and (tiles[i].vertices[2] == darts[0][0].vertices[3]):
                        new_left_kite.draw_kite(left_kite, 'top-right')
                        if not check_if_tile_exists(new_left_kite, list_of_all_tiles):
                            list_of_all_tiles.append(new_left_kite)
                            dictionary[key].append((new_left_kite, 3))

                        new_right_kite.draw_kite(right_kite, 'top-left')
                        if not check_if_tile_exists(new_right_kite, list_of_all_tiles):
                            list_of_all_tiles.append(new_right_kite)
                            dictionary[key].append((new_right_kite, 1))
                        print('drawing queen...')
                        return
                    elif (tiles[i].name == 'kite' and indices[i] == 3) and (tiles[i].vertices[2] == darts[0][0].vertices[2]):
                        new_left_kite.draw_kite(left_kite, 'top-right')
                        if not check_if_tile_exists(new_left_kite, list_of_all_tiles):
                            list_of_all_tiles.append(new_left_kite)
                            dictionary[key].append((new_left_kite, 3))

                        new_right_kite.draw_kite(right_kite, 'top-left')
                        if not check_if_tile_exists(new_right_kite, list_of_all_tiles):
                            list_of_all_tiles.append(new_right_kite)
                            dictionary[key].append((new_right_kite, 1))
                        print('drawing queen...')
                        return
            if len(kites) == 3:
                dart = darts[0][0]

                kite1 = Tile('kite')

                # missing top right kite
                kite1.draw_kite(dart, 'top-right')
                if kite1 in list_of_all_tiles:
                    kite2 = Tile('kite')
                    kite2.draw_kite(dart, 'top-left')
                    if kite2 in list_of_all_tiles:
                        kite3 = Tile('kite')
                        kite3.draw_kite(kite2, 'top-right')
                        if kite3 in list_of_all_tiles:
                            new_kite = Tile('kite')
                            new_kite.draw_kite(kite1, 'top-left')
                            if not check_if_tile_exists(new_kite, list_of_all_tiles):
                                list_of_all_tiles.append(new_kite)
                                dictionary[key].append((new_kite, 1))
                                return

                # missing top left kite
                kite1.draw_kite(dart, 'top-left')
                if kite1 in list_of_all_tiles:
                    kite2 = Tile('kite')
                    kite2.draw_kite(dart, 'top-right')
                    if kite2 in list_of_all_tiles:
                        kite3 = Tile('kite')
                        kite3.draw_kite(kite2, 'top-left')
                        if kite3 in list_of_all_tiles:
                            new_kite = Tile('kite')
                            new_kite.draw_kite(kite1, 'top-right')
                            if not check_if_tile_exists(new_kite, list_of_all_tiles):
                                list_of_all_tiles.append(new_kite)
                                dictionary[key].append((new_kite, 3))
                                return

                # counter-clockwise
                kite1.draw_kite(dart, 'top-right')
                if kite1 in list_of_all_tiles:
                    kite2 = Tile('kite')
                    kite2.draw_kite(kite1, 'top-left')
                    if kite2 in list_of_all_tiles:
                        kite3 = Tile('kite')
                        kite3.draw_kite(kite2, 'bottom-right')
                        if kite3 in list_of_all_tiles:
                            new_kite = Tile('kite')
                            new_kite.draw_kite(dart, 'top-left')
                            if not check_if_tile_exists(new_kite, list_of_all_tiles):
                                list_of_all_tiles.append(new_kite)
                                dictionary[key].append((new_kite, 1))
                            return

                # clockwise
                kite1.draw_kite(dart, 'top-left')
                if kite1 in list_of_all_tiles:
                    kite2 = Tile('kite')
                    kite2.draw_kite(kite1, 'top-right')
                    if kite2 in list_of_all_tiles:
                        kite3 = Tile('kite')
                        kite3.draw_kite(kite2, 'bottom-left')
                        if kite3 in list_of_all_tiles:
                            new_kite = Tile('kite')
                            new_kite.draw_kite(dart, 'top-right')
                            if not check_if_tile_exists(new_kite, list_of_all_tiles):
                                list_of_all_tiles.append(new_kite)
                                dictionary[key].append((new_kite, 3))
                                return

        elif sorted([('kite', 1), ('kite', 3), ('kite', 3)]) == sorted(vertex):
            v1_kite = None
            for kite in kites:
                if kite[1] == 1:
                    v1_kite = kite[0]
                    break
            if v1_kite is None:
                return

            temp_kite = Tile('kite')
            new_kite = Tile('kite')
            new_dart = Tile('dart')

            temp_kite.draw_kite(v1_kite, 'bottom-right')

            new_kite.draw_kite(temp_kite, 'top-left')
            if not check_if_tile_exists(new_kite, list_of_all_tiles):
                list_of_all_tiles.append(new_kite)
                dictionary[key].append((new_kite, 1))

            new_dart.draw_dart(new_kite, 'bottom-right')
            if not check_if_tile_exists(new_dart, list_of_all_tiles):
                list_of_all_tiles.append(new_dart)
                dictionary[key].append((new_dart, 0))
            return
        elif sorted([('kite', 1), ('kite', 1), ('kite', 3)]) == sorted(vertex):
            v3_kite = None
            for kite in kites:
                if kite[1] == 3:
                    v3_kite = kite[0]
                    break
            if v3_kite is None:
                return

            temp_kite = Tile('kite')
            new_kite = Tile('kite')
            new_dart = Tile('dart')

            temp_kite.draw_kite(v3_kite, 'bottom-left')

            new_kite.draw_kite(temp_kite, 'top-right')
            if not check_if_tile_exists(new_kite, list_of_all_tiles):
                list_of_all_tiles.append(new_kite)
                dictionary[key].append((new_kite, 3))

            new_dart.draw_dart(new_kite, 'bottom-left')
            if not check_if_tile_exists(new_dart, list_of_all_tiles):
                list_of_all_tiles.append(new_dart)
                dictionary[key].append((new_dart, 0))
            return
        elif sorted([('kite', 1), ('kite', 1), ('kite', 3), ('kite', 3)]) == sorted(vertex):
            print('Final Queen\'s case still needs to be implemented')
            print('Although I\'ve never seen this triggered')
            return


def king(key, dictionary_value, list_of_all_tiles, dictionary):
    if 3 <= len(dictionary_value) < 5:
        tiles, indices = sparse_vertex_dictionary_value(dictionary_value)
        darts = []
        kites = []
        vertex = []
        for i in range(len(tiles)):
            vertex.append((tiles[i].name, indices[i]))
            if tiles[i].name == 'dart':
                darts.append((tiles[i], indices[i]))
            if tiles[i].name == 'kite':
                kites.append((tiles[i], indices[i]))

        if len(darts) == 3 and len(kites) == 1:
            new_kite = Tile('kite')
            if kites[0][1] == 1:
                new_kite.draw_kite(kites[0][0], 'top-right')
                list_of_all_tiles.append(new_kite)
                dictionary[key].append((new_kite, 3))
            elif kites[0][1] == 3:
                new_kite.draw_kite(kites[0][0], 'top-left')
                if not check_if_tile_exists(new_kite, list_of_all_tiles):
                    list_of_all_tiles.append(new_kite)
                    dictionary[key].append((new_kite, 1))
            return
        if len(darts) == 2 and len(kites) == 2:
            right_dart = None
            for dart in darts:
                for kite in kites:
                    if kite[0].vertices[2] == dart[0].vertices[3]:
                        right_dart = dart[0]
                        break
                if right_dart is not None:
                    break

            if right_dart is not None:
                new_dart = Tile('dart')
                new_dart.draw_dart(right_dart, 'top-right')
                if not check_if_tile_exists(new_dart, list_of_all_tiles):
                    list_of_all_tiles.append(new_dart)
                    dictionary[key].append((new_dart, 0))


def force_tiles(dictionary, list_of_all_tiles):
    total = dictionary.copy()
    for key, value in total.items():
        ace(key, value, list_of_all_tiles, dictionary)
        deuce(key, value, list_of_all_tiles, dictionary)
        sun(key, value, list_of_all_tiles, dictionary)
        star(key, value, list_of_all_tiles, dictionary)
        jack(key, value, list_of_all_tiles, dictionary)
        prince(key, value, list_of_all_tiles, dictionary)
        queen(key, value, list_of_all_tiles, dictionary)
        king(key, value, list_of_all_tiles, dictionary)

        update_dictionary(dictionary, list_of_all_tiles)
    if not (total == dictionary):
        force_tiles(dictionary, list_of_all_tiles)


#
#
# -------------- Game Loop ----------------
#
while game_is_running:

    # Background color
    screen.fill((0, 0, 0))

    # Stop if too many tiles are created
    if len(all_tiles) >= 800:
        print('Too many Tiles; Ending program...')
        pygame.time.wait(30000)
        game_is_running = False

    # Event handler
    for event in pygame.event.get():
        # Exit
        if event.type == pygame.QUIT:
            game_is_running = False

        if event.type == pygame.MOUSEBUTTONUP:
            created_tile = create_new_tile(all_tiles)
            if created_tile is None:
                print('tile already exists')
            else:
                # Append new tile
                all_tiles.append(created_tile)
                # Update vertex dictionary
                update_dictionary(vertex_dictionary, list_of_all_tiles=all_tiles)
                # Check for forced tiles
                force_tiles(vertex_dictionary, list_of_all_tiles=all_tiles)
                print('tiles generated: ', len(all_tiles))
                print('------------------------------')
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                print('Next shape: dart') if kite_is_selected else print('Next shape: kite')
                kite_is_selected = not kite_is_selected
            if event.key == pygame.K_z:
                if len(all_tiles) > 1:
                    tile_to_remove = all_tiles[-1]
                    vertex_dictionary[tile_to_remove.vertices[0]].remove((tile_to_remove, 0))
                    vertex_dictionary[tile_to_remove.vertices[1]].remove((tile_to_remove, 1))
                    vertex_dictionary[tile_to_remove.vertices[2]].remove((tile_to_remove, 2))
                    vertex_dictionary[tile_to_remove.vertices[3]].remove((tile_to_remove, 3))
                    all_tiles.pop()

    for t in all_tiles:
        pygame.draw.polygon(screen, t.color, t.vertices)

    pygame.display.update()
