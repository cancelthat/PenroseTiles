import pygame
import math

from kite import Kite
from dart import Dart
from vertexTest import Vertex

dictionary_of_all_unique_possibilities = {(('dart', 2),): 'ace',
                                          (('dart', 2), ('kite', 1)): 'ace',
                                          (('dart', 2), ('kite', 3)): 'ace',
                                          (('dart', 2), ('kite', 1), ('kite', 3)): 'ace',

                                          (('kite', 2), ('kite', 2), ('kite', 2)): 'sun',
                                          (('kite', 2), ('kite', 2), ('kite', 2), ('kite', 2)): 'sun',
                                          (('kite', 2), ('kite', 2), ('kite', 2), ('kite', 2), ('kite', 2)): 'sun',

                                          (('dart', 0), ('dart', 0), ('dart', 0), ('dart', 0)): 'star',
                                          (('dart', 0), ('dart', 0), ('dart', 0), ('dart', 0), ('dart', 0)): 'star',

                                          (('kite', 0), ('kite', 0)): 'deuce',
                                          (('dart', 1), ('kite', 0), ('kite', 0)): 'deuce',
                                          (('dart', 3), ('kite', 0), ('kite', 0)): 'deuce',
                                          (('dart', 1), ('dart', 3), ('kite', 0), ('kite', 0)): 'deuce',

                                          (('dart', 1), ('kite', 2)): 'jack',
                                          (('dart', 3), ('kite', 2)): 'jack',
                                          (('kite', 0), ('kite', 2)): 'jack',
                                          (('dart', 1), ('kite', 2), ('kite', 2)): 'jack',
                                          (('dart', 3), ('kite', 2), ('kite', 2)): 'jack',
                                          (('dart', 1), ('dart', 3), ('kite', 2)): 'jack',
                                          (('dart', 1), ('kite', 0), ('kite', 2)): 'jack',
                                          (('dart', 3), ('kite', 0), ('kite', 2)): 'jack',
                                          (('kite', 0), ('kite', 2), ('kite', 2)): 'jack',
                                          (('dart', 1), ('dart', 3), ('kite', 0), ('kite', 2)): 'jack',
                                          (('dart', 1), ('dart', 3), ('kite', 2), ('kite', 2)): 'jack',
                                          (('dart', 1), ('kite', 0), ('kite', 2), ('kite', 2)): 'jack',
                                          (('dart', 3), ('kite', 0), ('kite', 2), ('kite', 2)): 'jack',
                                          (('dart', 1), ('dart', 3), ('kite', 0), ('kite', 2), ('kite', 2)): 'jack',

                                          (('kite', 1), ('kite', 1)): 'queen',
                                          (('kite', 3), ('kite', 3)): 'queen',
                                          (('kite', 1), ('kite', 1), ('kite', 3)): 'queen',
                                          (('kite', 1), ('kite', 3), ('kite', 3)): 'queen',
                                          (('dart', 0), ('kite', 1), ('kite', 1)): 'queen',
                                          (('dart', 0), ('kite', 3), ('kite', 3)): 'queen',
                                          (('dart', 0), ('kite', 1), ('kite', 1), ('kite', 3)): 'queen',
                                          (('dart', 0), ('kite', 1), ('kite', 3), ('kite', 3)): 'queen',
                                          (('kite', 1), ('kite', 1), ('kite', 3), ('kite', 3)): 'queen',
                                          (('dart', 0), ('kite', 1), ('kite', 1), ('kite', 3), ('kite', 3)): 'queen',

                                          (('dart', 0), ('dart', 0), ('kite', 1)): 'king',
                                          (('dart', 0), ('dart', 0), ('kite', 3)): 'king',
                                          (('dart', 0), ('dart', 0), ('kite', 1), ('kite', 3)): 'king',
                                          (('dart', 0), ('dart', 0), ('dart', 0), ('kite', 1)): 'king',
                                          (('dart', 0), ('dart', 0), ('dart', 0), ('kite', 3)): 'king',
                                          (('dart', 0), ('dart', 0), ('dart', 0), ('kite', 1), ('kite', 3)): 'king',

                                          (('dart', 0), ('kite', 1)): 'prince',
                                          (('dart', 0), ('kite', 3)): 'prince',

                                          (('dart', 0), ('kite', 1), ('kite', 3)): 'king-queen',
                                          (('dart', 1), ('dart', 3), ('kite', 0)): 'deuce-jack'}


def force_tiles(all_tiles, all_vertices):
    while True:

        tiles_len = len(all_tiles)

        # Create a list of all edge vertices
        edge_vertices = []
        for vertex in all_vertices:
            if vertex.name == 'edge':
                edge_vertices.append(vertex)

        # Create a key for the dictionary
        for edge_vertex in edge_vertices:
            set_ = []
            for vert in edge_vertex.vertex_components:
                set_.append((vert[0].name, vert[1]))
            set_.sort()

            vertex_key = dictionary_of_all_unique_possibilities.get(tuple(set_))
            if vertex_key is not None:
                if vertex_key == 'ace':
                    edge_vertex.name = 'ace'
                    dart = None
                    kite1, kite3 = None, None
                    for val in edge_vertex.vertex_components:
                        if val[0].name == 'dart':
                            dart = val[0]
                        elif val[1] == 1:
                            kite1 = val[0]
                        else:
                            kite3 = val[0]

                    if kite1 is None:
                        add_kite(dart, 'bottom-left', all_tiles, all_vertices)

                    if kite3 is None:
                        add_kite(dart, 'bottom-right', all_tiles, all_vertices)

                elif vertex_key == 'deuce':
                    edge_vertex.name = 'deuce'
                    right_kite = left_kite = None
                    dart1 = dart3 = None

                    for val in edge_vertex.vertex_components:
                        if val[0].name == 'kite':
                            if right_kite is None:
                                right_kite = val[0]
                            else:
                                left_kite = val[0]
                        elif val[1] == 1:
                            dart1 = val[0]
                        else:
                            dart3 = val[0]

                    if right_kite.vertices[1] == left_kite.vertices[3]:
                        holder = right_kite
                        right_kite = left_kite
                        left_kite = holder

                    if dart1 is None:
                        add_dart(left_kite, 'top-left', all_tiles, all_vertices)
                    if dart3 is None:
                        add_dart(right_kite, 'top-right', all_tiles, all_vertices)

                elif vertex_key == 'star':
                    edge_vertex.name = 'star'

                    darts = []
                    for val in edge_vertex.vertex_components:
                        darts.append(val[0])

                    for adj in edge_vertex.adjacent_vertices:
                        adj_darts = []  # list of kites contained in each of the sun's adjacent vertices
                        for comp in adj.vertex_components:
                            if comp[0].name == 'dart':
                                adj_darts.append(comp[0])

                        if len(set(darts) & set(adj_darts)) == 1:
                            dart = (set(darts) & set(adj_darts)).pop()
                            if dart.vertices.index(adj) == 1:
                                add_dart(dart, 'top-right', all_tiles, all_vertices)

                elif vertex_key == 'sun':
                    edge_vertex.name = 'sun'

                    kites = []  # list of kites contained in the sun vertex
                    for val in edge_vertex.vertex_components:
                        kites.append(val[0])

                    for adj in edge_vertex.adjacent_vertices:
                        adj_kites = []  # list of kites contained in each of the sun's adjacent vertices
                        for comp in adj.vertex_components:
                            if comp[0].name == 'kite':
                                adj_kites.append(comp[0])

                        if len(set(kites) & set(adj_kites)) == 1:
                            item = (set(kites) & set(adj_kites)).pop()
                            if len(kites) == 3:
                                if item.vertices.index(adj) == 1:
                                    add_kite(item, 'bottom-right', all_tiles, all_vertices)
                                elif item.vertices.index(adj) == 3:
                                    add_kite(item, 'bottom-left', all_tiles, all_vertices)
                            elif len(kites) == 4:
                                if item.vertices.index(adj) == 1:
                                    add_kite(item, 'bottom-right', all_tiles, all_vertices)

                elif vertex_key == 'jack':
                    edge_vertex.name = 'jack'
                    dart1 = dart3 = kite0 = left_kite = right_kite = None
                    for val in edge_vertex.vertex_components:
                        if val[0].name == 'dart':
                            if val[1] == 1:
                                dart1 = val[0]
                            else:
                                dart3 = val[0]
                        else:
                            if val[1] == 0:
                                kite0 = val[0]
                            else:
                                if left_kite is None:
                                    left_kite = val[0]
                                else:
                                    right_kite = val[0]

                    # Establish dart1, dart3, and kite0
                    if kite0 is None:
                        if dart3 is None:  # dart1
                            kite0 = add_kite(dart1, 'bottom-right', all_tiles, all_vertices)
                            dart3 = add_dart(kite0, 'top-right', all_tiles, all_vertices)
                        if dart1 is None:  # dart3
                            kite0 = add_kite(dart3, 'bottom-left', all_tiles, all_vertices)
                            dart1 = add_dart(kite0, 'top-left', all_tiles, all_vertices)
                    else:
                        if dart1 is None:
                            dart1 = add_dart(kite0, 'top-left', all_tiles, all_vertices)
                        if dart3 is None:
                            add_dart(kite0, 'top-right', all_tiles, all_vertices)

                    if right_kite is None:
                        if left_kite.vertices[3] == dart1.vertices[0]:
                            add_kite(left_kite, 'bottom-right', all_tiles, all_vertices)
                        else:
                            add_kite(left_kite, 'bottom-left', all_tiles, all_vertices)

                elif vertex_key == 'queen':
                    edge_vertex.name = 'queen'
                    dart = kite1a = kite1b = kite3a = kite3b = None
                    for val in edge_vertex.vertex_components:
                        if val[0].name == 'kite':
                            if val[1] == 1:
                                if kite1a is None:
                                    kite1a = val[0]
                                else:
                                    kite1b = val[0]
                            else:
                                if kite3a is None:
                                    kite3a = val[0]
                                else:
                                    kite3b = val[0]
                        else:
                            dart = val[0]

                    if kite1a is not None and kite1b is not None:
                        if kite3a is None:  # very low chance, my even be impossible of triggering
                            kite3a = add_kite(kite1a, 'top-right', all_tiles, all_vertices)
                            kite3b = add_kite(kite1b, 'top-right', all_tiles, all_vertices)

                        if kite3b is None:
                            if kite1a.vertices[2] == kite3a.vertices[2]:
                                kite3b = add_kite(kite1a, 'top-right', all_tiles, all_vertices)
                            elif kite1b.vertices[2] == kite3a.vertices[2]:
                                kite3b = add_kite(kite1b, 'top-right', all_tiles, all_vertices)
                            else:
                                if kite1a.vertices[0] == kite3a.vertices[0]:
                                    kite3b = add_kite(kite1b, 'top-right', all_tiles, all_vertices)
                                else:
                                    kite3b = add_kite(kite1a, 'top-right', all_tiles, all_vertices)

                    elif kite3a is not None and kite3b is not None:
                        if kite1a is None:
                            kite1a = add_kite(kite3a, 'top-left', all_tiles, all_vertices)
                            kite1b = add_kite(kite3b, 'top-left', all_tiles, all_vertices)
                        if kite1b is None:
                            if kite1a.vertices[2] == kite3a.vertices[2]:
                                kite1b = add_kite(kite3a, 'top-left', all_tiles, all_vertices)
                            elif kite1a.vertices[2] == kite3b.vertices[2]:
                                kite1b = add_kite(kite3b, 'top-left', all_tiles, all_vertices)
                            else:
                                if kite1a.vertices[0] == kite3a.vertices[0]:
                                    kite1b = add_kite(kite3b, 'top-left', all_tiles, all_vertices)
                                else:
                                    kite1b = add_kite(kite3a, 'top-left', all_tiles, all_vertices)

                    if dart is None:
                        if kite1a.vertices[2] == kite3b.vertices[2]:
                            add_dart(kite1b, 'bottom-right', all_tiles, all_vertices)
                        elif kite1b.vertices[2] == kite3a.vertices[2]:
                            add_dart(kite1a, 'bottom-right', all_tiles, all_vertices)
                        elif kite1a.vertices[2] == kite3a.vertices[2]:
                            add_dart(kite1b, 'bottom-right', all_tiles, all_vertices)
                        elif kite1b.vertices[2] == kite3b.vertices[2]:
                            add_dart(kite1a, 'bottom-right', all_tiles, all_vertices)

                    # I'm getting one extra vertex when I create the queen vertex. Not sure what' causing it.

                elif vertex_key == 'king':
                    edge_vertex.name = 'king'

                    kite1 = kite3 = dart_a = dart_b = dart_c = None
                    for val in edge_vertex.vertex_components:
                        if val[0].name == 'kite':
                            if val[1] == 1:
                                kite1 = val[0]
                            else:
                                kite3 = val[0]
                        else:
                            if dart_a is None:
                                dart_a = val[0]
                            elif dart_b is None:
                                dart_b = val[0]
                            else:
                                dart_c = val[0]

                    # Establish kites
                    if kite1 is None:
                        kite1 = add_kite(kite3, 'top-left', all_tiles, all_vertices)
                    elif kite3 is None:
                        kite3 = add_kite(kite1, 'top-right', all_tiles, all_vertices)

                    if dart_c is None:

                        kite1_v2_components = []
                        kite3_v2_components = []
                        for v in kite1.vertices[2].vertex_components:
                            kite1_v2_components.append(v[0])
                        for v in kite3.vertices[2].vertex_components:
                            kite3_v2_components.append(v[0])
                        darts = [dart_a, dart_b]
                        if len(set(kite1_v2_components) & set(darts)) == 0:
                            add_dart(kite1, 'bottom-right', all_tiles, all_vertices)
                        elif len(set(kite3_v2_components) & set(darts)) == 0:
                            add_dart(kite3, 'bottom-left', all_tiles, all_vertices)
                        else:
                            add_dart((set(kite1_v2_components) & set(darts)).pop(), 'top-right',
                                     all_tiles, all_vertices)

                elif vertex_key == 'prince':

                    kite1 = kite3 = None
                    for val in edge_vertex.vertex_components:
                        if val[0].name == 'kite':
                            if val[1] == 1:
                                kite1 = val[0]
                            else:
                                kite3 = val[0]

                    if kite1 is None:
                        add_kite(kite3, 'top-left', all_tiles, all_vertices)
                    else:
                        add_kite(kite1, 'top-right', all_tiles, all_vertices)

                elif vertex_key == 'deuce-jack':
                    dart1 = dart3 = None
                    for val in edge_vertex.vertex_components:
                        if val[0].name == 'dart':
                            if val[1] == 1:
                                dart1 = val[0]
                            else:
                                dart3 = val[0]

                    if dart1.vertices[0] == dart3.vertices[0]:
                        pass
                    else:
                        edge_vertex.name = 'jack'
                        add_kite(dart1, 'top-right', all_tiles, all_vertices)
                        add_kite(dart3, 'top-left', all_tiles, all_vertices)

                elif vertex_key == 'king-queen':
                    kite1 = kite3 = dart0 = None
                    for val in edge_vertex.vertex_components:
                        if val[0].name == 'kite':
                            if val[1] == 1:
                                kite1 = val[0]
                            else:
                                kite3 = val[0]
                        else:
                            dart0 = val[0]

                    if kite1.vertices[2] == dart0.vertices[3] and kite3.vertices[2] == dart0.vertices[1]:
                        edge_vertex.name = 'queen'
                        add_kite(kite1, 'top-right', all_tiles, all_vertices)
                        add_kite(kite3, 'top-left', all_tiles, all_vertices)

                else:
                    print('error:', vertex_key, edge_vertex.vertex_components)
    # Need to get rid of the compare_coordinates function and search through adjacent vertices
        if tiles_len == len(all_tiles) or len(all_tiles) > 12500:
            break


# ------------------ Helper functions ------------------

# Because of the floating point rounding error, coordinates need to be compared with a tolerance.
# default: 0.001 error tolerance with 6 point rounding accuracy
def compare_coordinates(first, other):
    value = (first[0] - other[0]) + (first[1] - other[1])
    if abs(value) < 0.0000001:
        return True
    return False


# Determines if a Vertex has a neighbor at a given point, and returns the neighboring Vertex if found.
def traverse_adjacent_vertices(coordinates, vertex):
    for adj_vertex in vertex.adjacent_vertices:
        if compare_coordinates(coordinates, adj_vertex.coordinates):
            return adj_vertex
    return False


# Distance from a point to the cursor
def dist(p):
    x, y = pygame.mouse.get_pos()
    return math.sqrt((p[0] - x) ** 2 + (p[1] - y) ** 2)


def add_kite(neighbor_tile, direction, tiles, vertices):
    new_tile = Kite()
    new_tile.draw(neighbor_tile, direction)

    g0, g1, g2, g3 = neighbor_tile.vertices
    h0, h1, h2, h3 = new_tile.vertex_coordinates
    v0 = v1 = v2 = v3 = False
    if neighbor_tile.name == 'kite':
        if direction == 'top-right':
            v0 = g0
            v1 = vertex_exists(h1, g0)
            v2 = vertex_exists(h2, g1)
            v3 = g1
        elif direction == 'bottom-right':
            v0 = vertex_exists(h0, g1)
            v1 = vertex_exists(h1, g2)
            v2 = g2
            v3 = g1
        elif direction == 'bottom-left':
            v0 = vertex_exists(h0, g3)
            v1 = g3
            v2 = g2
            v3 = vertex_exists(h3, g2)
        elif direction == 'top-left':
            v0 = g0
            v1 = g3
            v2 = vertex_exists(h2, g3)
            v3 = vertex_exists(h3, g0)

    elif neighbor_tile.name == 'dart':
        if direction == 'top-right':
            v0 = vertex_exists(h0, g0)
            v1 = vertex_exists(h1, g1)
            v2 = g1
            v3 = g0
        elif direction == 'bottom-right':
            v0 = g1
            v1 = vertex_exists(h1, g1)
            v2 = vertex_exists(h2, g2)
            v3 = g2
        elif direction == 'bottom-left':
            v0 = g3
            v1 = g2
            v2 = vertex_exists(h2, g2)
            v3 = vertex_exists(h3, g3)
        elif direction == 'top-left':
            v0 = vertex_exists(h0, g0)
            v1 = g0
            v2 = g3
            v3 = vertex_exists(h3, g3)

    tiles.append(new_tile)
    new_vertices, vertices_to_add = link_vertices([v0, v1, v2, v3], new_tile)
    new_tile.vertices = new_vertices
    vertices.extend(vertices_to_add)

    return new_tile


def add_dart(neighbor_tile, direction, tiles, vertices):
    new_tile = Dart()
    new_tile.draw(neighbor_tile, direction)

    g0, g1, g2, g3 = neighbor_tile.vertices
    h0, h1, h2, h3 = new_tile.vertex_coordinates
    v0 = v1 = v2 = v3 = False
    if neighbor_tile.name == 'kite':
        if direction == 'top-right':
            v0 = vertex_exists(h0, g0)
            v1 = vertex_exists(h1, g1)
            v2 = g1
            v3 = g0
        elif direction == 'bottom-right':
            v0 = g1
            v1 = vertex_exists(h1, g1)
            v2 = vertex_exists(h2, g2)
            v3 = g2
        elif direction == 'bottom-left':
            v0 = g3
            v1 = g2
            v2 = vertex_exists(h2, g2)
            v3 = vertex_exists(h3, g3)
        elif direction == 'top-left':
            v0 = vertex_exists(h0, g0)
            v1 = g0
            v2 = g3
            v3 = vertex_exists(h3, g3)

    elif neighbor_tile.name == 'dart':
        if direction == 'top-right':
            v0 = g0
            v1 = vertex_exists(h1, g0)
            v2 = vertex_exists(h2, g1)
            v3 = g1
        elif direction == 'top-left':
            v0 = g0
            v1 = g3
            v2 = vertex_exists(h2, g3)
            v3 = vertex_exists(h3, g0)
        else:
            print('error in direction: ', direction)

    tiles.append(new_tile)
    new_vertices, vertices_to_add = link_vertices([v0, v1, v2, v3], new_tile)
    new_tile.vertices = new_vertices
    vertices.extend(vertices_to_add)

    return new_tile


def link_vertices(new_vertices, new_tile):
    v0, v1, v2, v3 = new_vertices
    n0, n1, n2, n3 = new_tile.vertex_coordinates
    return_vertices = []
    if bool(v0) + bool(v1) + bool(v2) + bool(v3) == 2:  # Need to figure out the single False condition
        if (not v0 and not v1) or (not v2 and not v3):
            switch = True if not v0 or not v1 else False
            if not v0:
                v0 = Vertex(n0, [v3])
                return_vertices.append(v0)
                v3.adjacent_vertices.append(v0)
            if not v1:
                v1 = Vertex(n1, [v2])
                return_vertices.append(v1)
                v2.adjacent_vertices.append(v1)
            if not v2:
                v2 = Vertex(n2, [v1])
                return_vertices.append(v2)
                v1.adjacent_vertices.append(v2)
            if not v3:
                v3 = Vertex(n3, [v0])
                return_vertices.append(v3)
                v0.adjacent_vertices.append(v3)

            if switch:
                v0.adjacent_vertices.append(v1)
                v1.adjacent_vertices.append(v0)
            else:
                v2.adjacent_vertices.append(v3)
                v3.adjacent_vertices.append(v2)

        elif (not v1 and not v2) or (not v0 and not v3):
            switch = True if not v1 or not v2 else False
            if not v0:
                v0 = Vertex(n0, [v1])
                return_vertices.append(v0)
                v1.adjacent_vertices.append(v0)
            if not v1:
                v1 = Vertex(n1, [v0])
                return_vertices.append(v1)
                v0.adjacent_vertices.append(v1)
            if not v2:
                v2 = Vertex(n2, [v3])
                return_vertices.append(v2)
                v3.adjacent_vertices.append(v2)
            if not v3:
                v3 = Vertex(n3, [v2])
                return_vertices.append(v3)
                v2.adjacent_vertices.append(v3)

            if switch:
                v1.adjacent_vertices.append(v2)
                v2.adjacent_vertices.append(v1)
            else:
                v0.adjacent_vertices.append(v3)
                v3.adjacent_vertices.append(v0)

    elif bool(v0) + bool(v1) + bool(v2) + bool(v3) == 3:
        if not v0:
            neighbor0 = vertex_exists(n0, v1)
            neighbor1 = vertex_exists(n0, v3)
            if neighbor0:
                v0 = neighbor0
                v0.adjacent_vertices.append(v3)
                v3.adjacent_vertices.append(v0)
            elif neighbor1:
                v0 = neighbor1
                v0.adjacent_vertices.append(v1)
                v1.adjacent_vertices.append(v0)
            else:
                v0 = Vertex(n0, [v1, v3])
                return_vertices.append(v0)
                v1.adjacent_vertices.append(v0)
                v3.adjacent_vertices.append(v0)
        elif not v1:
            neighbor0 = vertex_exists(n1, v0)
            neighbor1 = vertex_exists(n1, v2)
            if neighbor0:
                v1 = neighbor0
                v1.adjacent_vertices.append(v2)
                v2.adjacent_vertices.append(v1)
            elif neighbor1:
                v1 = neighbor1
                v1.adjacent_vertices.append(v0)
                v0.adjacent_vertices.append(v1)
            else:
                v1 = Vertex(n1, [v0, v2])
                return_vertices.append(v1)
                v0.adjacent_vertices.append(v1)
                v2.adjacent_vertices.append(v1)
        elif not v2:
            neighbor0 = vertex_exists(n2, v1)
            neighbor1 = vertex_exists(n2, v3)
            if neighbor0:
                v2 = neighbor0
                v2.adjacent_vertices.append(v3)
                v3.adjacent_vertices.append(v2)
            elif neighbor1:
                v2 = neighbor1
                v2.adjacent_vertices.append(v1)
                v1.adjacent_vertices.append(v2)
            else:
                v2 = Vertex(n2, [v1, v3])
                return_vertices.append(v2)
                v1.adjacent_vertices.append(v2)
                v3.adjacent_vertices.append(v2)
        elif not v3:
            neighbor0 = vertex_exists(n3, v0)
            neighbor1 = vertex_exists(n3, v2)
            if neighbor0:
                v3 = neighbor0
                v3.adjacent_vertices.append(v2)
                v2.adjacent_vertices.append(v3)
            elif neighbor1:
                v3 = neighbor1
                v3.adjacent_vertices.append(v0)
                v0.adjacent_vertices.append(v3)
            else:
                v3 = Vertex(n3, [v0, v2])
                return_vertices.append(v3)
                v0.adjacent_vertices.append(v3)
                v2.adjacent_vertices.append(v3)
        print(neighbor0, neighbor1) # always False False?

    elif bool(v0) + bool(v1) + bool(v2) + bool(v3) == 4:
        # I have a gut feeling that there may be an oversight here, such as not needing to link the vertices in some
        # cases, but I haven't verified whether that is true or not.
        switch0 = switch1 = switch2 = switch3 = 0
        for adjacent_vertex in v0.adjacent_vertices:
            if adjacent_vertex == v1 or adjacent_vertex == v3:
                switch0 += 1

        for adjacent_vertex in v1.adjacent_vertices:
            if adjacent_vertex == v0 or adjacent_vertex == v2:
                switch1 += 1

        for adjacent_vertex in v2.adjacent_vertices:
            if adjacent_vertex == v1 or adjacent_vertex == v3:
                switch2 += 1

        for adjacent_vertex in v3.adjacent_vertices:
            if adjacent_vertex == v0 or adjacent_vertex == v2:
                switch3 += 1

        if switch0 == 1:
            if v1 in v0.adjacent_vertices:
                v0.adjacent_vertices.append(v3)
            elif v3 in v0.adjacent_vertices:
                v0.adjacent_vertices.append(v1)

        if switch1 == 1:
            if v0 in v1.adjacent_vertices:
                v1.adjacent_vertices.append(v2)
            elif v2 in v1.adjacent_vertices:
                v1.adjacent_vertices.append(v0)

        if switch2 == 1:
            if v1 in v2.adjacent_vertices:
                v2.adjacent_vertices.append(v3)
            elif v3 in v2.adjacent_vertices:
                v2.adjacent_vertices.append(v1)

        if switch3 == 1:
            if v0 in v3.adjacent_vertices:
                v3.adjacent_vertices.append(v2)
            elif v2 in v3.adjacent_vertices:
                v3.adjacent_vertices.append(v0)

    else:
        print('eR%%ROR')

    v0.vertex_components.append((new_tile, 0))
    v1.vertex_components.append((new_tile, 1))
    v2.vertex_components.append((new_tile, 2))
    v3.vertex_components.append((new_tile, 3))

    return [v0, v1, v2, v3], return_vertices


def vertex_exists(coordinates, vertex_list, n=3):
    # print(n, vertex_list)
    if isinstance(vertex_list, list):
        searched_adjacent_vertices = vertex_list
    else:
        searched_adjacent_vertices = [vertex_list]

    if n == 0:
        return False

    for vertex in searched_adjacent_vertices.copy():
        for adj_vertex in vertex.adjacent_vertices:

            # return the vertex if found
            if compare_coordinates(coordinates, adj_vertex.coordinates):
                return adj_vertex
            else:
                # if the adjacent vertex is in the list, do not append.
                if adj_vertex not in searched_adjacent_vertices:
                    searched_adjacent_vertices.append(adj_vertex)

                    # this method will compare vertices that have already been compared, wasting resources. It could
                    # be updated to ignore those that have been searched, but as long as n is low, it shouldn't
                    # matter too much.

    return vertex_exists(coordinates, searched_adjacent_vertices, n-1)
