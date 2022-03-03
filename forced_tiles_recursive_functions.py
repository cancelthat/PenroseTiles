from kite import Kite
from dart import Dart
from vertex import Vertex


def new_force(vertices, tiles):

    tiles_len = len(tiles)
    if tiles_len > 5000:
        print('5000 vertex limit reached')
        return

    edge_vertices = []
    for vertex in vertices:
        if vertex.name == 'edge':
            edge_vertices.append(vertex)

    for edge_vertex in edge_vertices:
        if ace(edge_vertex, vertices, tiles):
            edge_vertex.name = 'ace'
            continue
        if queen(edge_vertex, vertices, tiles):
            edge_vertex.name = 'queen'
            continue
        if jack(edge_vertex, vertices, tiles):
            edge_vertex.name = 'jack'
            continue
        if deuce(edge_vertex, vertices, tiles):
            edge_vertex.name = 'deuce'
            continue
        if king(edge_vertex, vertices, tiles):
            edge_vertex.name = 'king'
            continue
        if star(edge_vertex, vertices, tiles):
            edge_vertex.name = 'star'
            continue
        if sun(edge_vertex, vertices, tiles):
            edge_vertex.name = 'sun'
            continue
        if prince(edge_vertex, vertices, tiles):
            continue
        pass

    if tiles_len != len(tiles):
        new_force(vertices, tiles)


def ace(vertex, all_vertices, all_tiles):

    if congruent(vertex, [('dart', 2)]):
        dart = None
        for val in vertex.congruent_vertices:
            if val[0].name == 'dart':
                dart = val[0]

        right_kite = Kite()
        right_kite.draw(dart, 'bottom-left')

        left_kite = Kite()
        left_kite.draw(dart, 'bottom-right')

        update_tiles([right_kite, left_kite], all_tiles, all_vertices)

        return True
    return False


def sun(vertex, all_vertices, all_tiles):
    if congruent(vertex, [('kite', 2), ('kite', 2), ('kite', 2), ('kite', 2)]):
        for val in vertex.congruent_vertices:
            new_tile = Kite()
            new_tile.draw(val[0], 'bottom-right')
            update_tiles(new_tile, all_tiles, all_vertices)

            if len(vertex.congruent_vertices) == 5:
                return True
    elif congruent(vertex, [('kite', 2), ('kite', 2), ('kite', 2)]):
        for val in vertex.congruent_vertices:
            tile_right = Kite()
            tile_right.draw(val[0], 'bottom-right')
            update_tiles(tile_right, all_tiles, all_vertices)
            if len(vertex.congruent_vertices) == 5:
                return True

            tile_left = Kite()
            tile_left.draw(val[0], 'bottom-left')
            update_tiles(tile_left, all_tiles, all_vertices)
            if len(vertex.congruent_vertices) == 5:
                return True
    return False


def star(vertex, all_vertices, all_tiles):
    if congruent(vertex, [('dart', 0), ('dart', 0), ('dart', 0), ('dart', 0)]):
        for val in vertex.congruent_vertices:
            new_tile = Dart()
            new_tile.draw(val[0], 'top-right')

            update_tiles(new_tile, all_tiles, all_vertices)

            if len(vertex.congruent_vertices) == 5:
                return True
    return False


def deuce(vertex, all_vertices, all_tiles):
    if congruent(vertex, [('kite', 0), ('kite', 0)]):
        k1, k2 = None, None
        for val in vertex.congruent_vertices:
            if val[0].name == 'kite':
                if k1 is None:
                    k1 = val[0]
                else:
                    k2 = val[0]

        new_left_dart = Dart()
        new_right_dart = Dart()

        if compare_coord(k1.vertices[1], k2.vertices[3]):
            new_left_dart.draw(k1, 'top-left')
            new_right_dart.draw(k2, 'top-right')
        else:
            new_left_dart.draw(k1, 'top-right')
            new_right_dart.draw(k2, 'top-left')

        update_tiles([new_left_dart, new_right_dart], all_tiles, all_vertices)
        return True
    return False


def jack(vertex, all_vertices, all_tiles):
    d1 = congruent(vertex, [('dart', 1)])
    d3 = congruent(vertex, [('dart', 3)])

    if d1 and d3:
        left_dart, right_dart = None, None
        for val in vertex.congruent_vertices:
            if val[0].name == 'dart':
                if val[1] == 1:
                    left_dart = val[0]
                elif val[1] == 3:
                    right_dart = val[0]

        # if the two darts are touching at vertex 0, then return (because a jack isn't possible)
        if compare_coord(left_dart.vertices[0], right_dart.vertices[0]):
            return False

        top_left_kite = Kite()
        top_right_kite = Kite()
        bottom_kite = Kite()

        top_left_kite.draw(left_dart, 'top-right')
        top_right_kite.draw(right_dart, 'top-left')
        bottom_kite.draw(left_dart, 'bottom-right')

        update_tiles([top_left_kite, top_right_kite, bottom_kite], all_tiles, all_vertices)
        return True
    elif congruent(vertex, [('kite', 2)]):
        if d1:
            dart = None
            for val in vertex.congruent_vertices:
                if val[0].name == 'dart':
                    dart = val[0]

            bottom_kite = Kite()
            new_dart = Dart()
            top_left_kite = Kite()
            top_right_kite = Kite()

            bottom_kite.draw(dart, 'bottom-right')
            new_dart.draw(bottom_kite, 'top-right')
            top_left_kite.draw(dart, 'top-right')
            top_right_kite.draw(top_left_kite, 'bottom-right')

            update_tiles([new_dart, top_left_kite, top_right_kite, bottom_kite], all_tiles, all_vertices)
            return True
        elif d3:
            dart = None
            for val in vertex.congruent_vertices:
                if val[0].name == 'dart':
                    dart = val[0]

            top_left_kite = Kite()
            top_right_kite = Kite()
            bottom_kite = Kite()
            new_dart = Dart()

            top_right_kite.draw(dart, 'top-left')
            top_left_kite.draw(top_right_kite, 'bottom-left')
            bottom_kite.draw(dart, 'bottom-left')
            new_dart.draw(bottom_kite, 'top-left')

            update_tiles([new_dart, top_left_kite, top_right_kite, bottom_kite], all_tiles, all_vertices)

            return True
    return False


def queen(vertex, all_vertices, all_tiles):
    # the second part says: if only a single (Dart, 0) exist in the congruent vertices
    if congruent(vertex, [('dart', 0), ('kite', 1), ('kite', 3)]) and not congruent(vertex, [('dart', 0), ('dart', 0)]):

        dart, k1, k3 = None, None, None
        for val in vertex.congruent_vertices:
            if val[0].name == 'dart':
                dart = val[0]
            elif (val[0].name, val[1]) == ('kite', 1):
                k1 = val[0]
            elif (val[0].name, val[1]) == ('kite', 3):
                k3 = val[0]

        # a kite needs to exist on both sides of the dart, otherwise it could be a king vertex.
        if compare_coord(k1.vertices[2], dart.vertices[3]) and compare_coord(k3.vertices[2], dart.vertices[1]):
            top_right_kite = Kite()
            top_left_kite = Kite()

            top_left_kite.draw(k1, 'top-right')
            top_right_kite.draw(k3, 'top-left')

            update_tiles([top_left_kite, top_right_kite], all_tiles, all_vertices)
            return True
    if congruent(vertex, [('kite', 1), ('kite', 1), ('kite', 3)]):
        k1_a, k1_b, k3 = None, None, None
        for val in vertex.congruent_vertices:
            if (val[0].name, val[1]) == ('kite', 1):
                if k1_a is None:
                    k1_a = val[0]
                else:
                    k1_b = val[0]
            elif val[0].name == 'kite' and val[1] == 3:
                k3 = val[0]

        temp_kite = Kite()
        new_dart = Dart()
        new_kite = Kite()
        if compare_coord(k3.vertices[2], k1_a.vertices[2]) or compare_coord(k3.vertices[2], k1_b.vertices[2]):
            # top left
            temp_kite.draw(k3, 'top-left')
            new_dart.draw(temp_kite, 'bottom-right')
            new_kite.draw(new_dart, 'top-right')
        else:
            # bottom right
            new_dart.draw(k3, 'bottom-left')
            temp_kite.draw(new_dart, 'top-left')
            new_kite.draw(temp_kite, 'top-right')

        update_tiles([new_dart, new_kite], all_tiles, all_vertices)
        return True
    elif congruent(vertex, [('kite', 1), ('kite', 3), ('kite', 3)]):
        k3_a, k3_b, k1 = None, None, None
        for val in vertex.congruent_vertices:
            if val[0].name == 'kite' and val[1] == 3:
                if k3_a is None:
                    k3_a = val[0]
                else:
                    k3_b = val[0]
            elif val[0].name == 'kite' and val[1] == 1:
                k1 = val[0]

        temp_kite = Kite()
        new_dart = Dart()
        new_kite = Kite()
        if compare_coord(k1.vertices[2], k3_a.vertices[2]) or compare_coord(k1.vertices[2], k3_b.vertices[2]):
            # top left
            temp_kite.draw(k1, 'top-right')
            new_dart.draw(temp_kite, 'bottom-left')
            new_kite.draw(new_dart, 'top-left')
        else:
            # bottom right
            new_dart.draw(k1, 'bottom-right')
            temp_kite.draw(new_dart, 'top-right')
            new_kite.draw(temp_kite, 'top-left')

        update_tiles([new_dart, new_kite], all_tiles, all_vertices)

        return True
    return False


def king(vertex, all_vertices, all_tiles):
    # if two (Dart, 0) and at least one (Kite, 1) or (Kite, 3) exist
    if congruent(vertex, [('dart', 0), ('dart', 0)]) and (congruent(vertex, [('kite', 1)]) or congruent(vertex, [('kite', 3)])):
        k1, k3 = None, None
        # only 1 kite is need, the rest of the tiles will be drawn and checked
        for val in vertex.congruent_vertices:
            if val[0].name == 'kite' and val[1] == 1:
                k1 = val[0]
                break
            if val[0].name == 'kite' and val[1] == 3:
                k3 = val[0]
                break

        if k1 is not None:
            kite = Kite()
            dart1, dart2, dart3 = Dart(), Dart(), Dart()

            kite.draw(k1, 'top-right')
            dart1.draw(k1, 'bottom-right')
            dart2.draw(dart1, 'top-right')
            dart3.draw(dart2, 'top-right')

            update_tiles([kite, dart1, dart2, dart3], all_tiles, all_vertices)
        else:
            kite = Kite()
            dart1, dart2, dart3 = Dart(), Dart(), Dart()

            kite.draw(k3, 'top-left')
            dart1.draw(k3, 'bottom-left')
            dart2.draw(dart1, 'top-left')
            dart3.draw(dart2, 'top-left')

            update_tiles([kite, dart1, dart2, dart3], all_tiles, all_vertices)
        return True
    return False


def prince(vertex, all_vertices, all_tiles):
    # A prince vertex has forced tiles, but is only partially completed. It consists of 1 dart and 2 kites.
    # Depending on which tile is placed next, the prince vertex will either become a King vertex or a Queen vertex.
    single_dart = congruent(vertex, [('dart', 0)]) and not congruent(vertex, [('dart', 0), ('dart', 0)])
    single_k1 = congruent(vertex, [('kite', 1)]) and not congruent(vertex, [('kite', 1), ('kite', 1)])
    single_k3 = congruent(vertex, [('kite', 3)]) and not congruent(vertex, [('kite', 3), ('kite', 3)])
    xor_kite = (not single_k1 and single_k3) or (single_k1 and not single_k3)
    # if a single dart and a single kite exist,
    if single_dart and xor_kite:
        dart, kite = None, None
        for val in vertex.congruent_vertices:
            if val[0].name == 'dart':
                dart = val[0]
            elif val[0].name == 'kite':
                kite = val[0]

        new_kite = Kite()
        if compare_coord(dart.vertices[1], kite.vertices[2]):
            new_kite.draw(kite, 'top-left')
            update_tiles(new_kite, all_tiles, all_vertices)
            return True
        elif compare_coord(dart.vertices[3], kite.vertices[2]):
            new_kite.draw(kite, 'top-right')
            update_tiles(new_kite, all_tiles, all_vertices)
            return True
    return False


# Checks if a vertex contains the values. The values being the congruent vertices of the form, ex. (Dart(), 1). A tuple
# with the first element being a Tile and the second element representing the Tile's vertex number.
def congruent(vertex=None, subset=None):
    if (vertex is None) or (subset is None):  # if empty
        return False
    set_ = []
    for vert in vertex.congruent_vertices:
        set_.append((vert[0].name, vert[1]))

    if all(x in set_ for x in subset):
        for thing in subset:
            try:
                set_.remove(thing)
            except ValueError:
                return False
            except AttributeError:
                return False
        return True
    return False


# 3 arithmetic, 1 comparison
def compare_coord(first, other):
    value = (first[0] - other[0]) + (first[1] - other[1])
    if abs(value) < 0.001:
        return True
    return False


# Function: 4 tile vertices loop through all vertices comparing coordinates
# Run Time: O(n): 4n
def update_vertices(tiles, vertices):
    t = []
    if isinstance(tiles, list):
        t = tiles
    else:
        t.append(tiles)

    for tile in t:
        # update the list of all vertices
        for tile_vertex in tile.vertices:
            # if the tile's vertex does not exist in the list of all vertices, then add it to the list.
            if not any(compare_coord(vertex.coordinates, tile_vertex) for vertex in vertices):
                new_vertex = Vertex(tile, tile_vertex)
                vertices.append(new_vertex)
                update_congruency(new_vertex, tile)
            else:
                # if it does exist, then update the existing vertex's congruency.
                vert = [vertex for vertex in vertices if compare_coord(vertex.coordinates, tile_vertex)]
                update_congruency(vert[0], tile)


# Function: tile.vertices(4) * vertex.congruent_vertices(4) = 16 calls, appends
# Run Time: O(1): 128 operations per tile
def update_congruency(vertex, tiles):
    t = []
    if isinstance(tiles, list):
        t = tiles
    else:
        t.append(tiles)

    for tile in t:
        # update the congruent vertices for vertex
        for index, tile_vertex in enumerate(tile.vertices):
            # if (tile, index) is not in congruent vertices
            if not (tile, index) in vertex.congruent_vertices:
                if compare_coord(vertex.coordinates, tile.vertices[index]):
                    vertex.congruent_vertices.append((tile, index))


# Function: loops through all_tiles, comparing tiles; tile __eq__ has 2 comparisons. If the tile does not exist, the
# function will loop through all of the tiles.
# Run Time: O(n)
def update_tiles(tiles, all_tiles, all_vertices):
    # update the list of all tiles
    if isinstance(tiles, list):
        flags = []
        for t in tiles:
            flag = 1
            for s in all_tiles:
                if s == t:
                    flag = 0
                    flags.append(False)
                    break
            if flag:
                update_vertices(t, all_vertices)
                all_tiles.append(t)
                flags.append(True)
        return flags
    else:
        if not (tiles in all_tiles):
            all_tiles.append(tiles)
            update_vertices(tiles, all_vertices)
            return True
        return False
