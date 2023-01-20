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

                    if right_kite.vertex_coordinates[1] == left_kite.vertex_coordinates[3]:
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

                    for dart in darts:
                        if len(dart.vertices[1].vertex_components) == 2:
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
                    pass

                else:
                    print('error:', vertex_key)

        if tiles_len == len(all_tiles):
            break


# ------------------ Helper functions ------------------

# Because of the floating point rounding error, coordinates need to be compared with a tolerance.
# default: 0.001 error tolerance with 6 point rounding accuracy
def compare_coordinates(first, other):
    value = (first[0] - other[0]) + (first[1] - other[1])
    if abs(value) < 0.001:
        return True
    return False


# Determines if a Vertex has a neighbor at a given point, and returns the neighboring Vertex if found.
def vertex_exists(coordinates, vertex):
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

    return "kite appended."


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

    return 'dart appended'


def link_vertices(new_vertices, new_tile):
    v0, v1, v2, v3 = new_vertices
    w0, w1, w2, w3 = new_tile.vertex_coordinates
    return_vertices = []
    if bool(v0) + bool(v1) + bool(v2) + bool(v3) == 2:  # Need to figure out the single False condition
        if (not v0 and not v1) or (not v2 and not v3):
            switch = True if not v0 or not v1 else False
            if not v0:
                v0 = Vertex(w0, [v3])
                return_vertices.append(v0)
                v3.adjacent_vertices.append(v0)
            if not v1:
                v1 = Vertex(w1, [v2])
                return_vertices.append(v1)
                v2.adjacent_vertices.append(v1)
            if not v2:
                v2 = Vertex(w2, [v1])
                return_vertices.append(v2)
                v1.adjacent_vertices.append(v2)
            if not v3:
                v3 = Vertex(w3, [v0])
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
                v0 = Vertex(w0, [v1])
                return_vertices.append(v0)
                v1.adjacent_vertices.append(v0)
            if not v1:
                v1 = Vertex(w1, [v0])
                return_vertices.append(v1)
                v0.adjacent_vertices.append(v1)
            if not v2:
                v2 = Vertex(w2, [v3])
                return_vertices.append(v2)
                v3.adjacent_vertices.append(v2)
            if not v3:
                v3 = Vertex(w3, [v2])
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
            v0 = Vertex(w0, [v1, v3])
            return_vertices.append(v0)
            v1.adjacent_vertices.append(v0)
            v3.adjacent_vertices.append(v0)
        elif not v1:
            v1 = Vertex(w1, [v0, v2])
            return_vertices.append(v1)
            v0.adjacent_vertices.append(v1)
            v2.adjacent_vertices.append(v1)
        elif not v2:
            v2 = Vertex(w2, [v1, v3])
            return_vertices.append(v2)
            v1.adjacent_vertices.append(v2)
            v3.adjacent_vertices.append(v2)
        elif not v3:
            v3 = Vertex(w3, [v0, v2])
            return_vertices.append(v3)
            v0.adjacent_vertices.append(v3)
            v2.adjacent_vertices.append(v3)

    elif bool(v0) + bool(v1) + bool(v2) + bool(v3) == 4:

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
