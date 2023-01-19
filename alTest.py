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
                        new_kite = Kite()
                        new_kite.draw(dart, 'bottom-left')
                        all_tiles.append(new_kite)

                        # Assign vertices
                        d0, d1, d2, d3 = dart.vertices
                        a0 = d3
                        a1 = d2
                        a2 = vertex_exists(new_kite.vertex_coordinates[2], d2)
                        a3 = vertex_exists(new_kite.vertex_coordinates[3], d3)

                        switch = True if not a2 or not a3 else False

                        # Create a new Vertex if nothing is found
                        if not a2:
                            a2 = Vertex(new_kite.vertex_coordinates[2], [a1])
                            all_vertices.append(a2)
                            a1.adjacent_vertices.append(a2)

                        if not a3:
                            a3 = Vertex(new_kite.vertex_coordinates[3], [a0])
                            all_vertices.append(a3)
                            a0.adjacent_vertices.append(a3)

                        if switch:
                            a2.adjacent_vertices.append(a3)
                            a3.adjacent_vertices.append(a2)

                        # Add vertex components
                        a0.vertex_components.append((new_kite, 0))
                        a1.vertex_components.append((new_kite, 1))
                        a2.vertex_components.append((new_kite, 2))
                        a3.vertex_components.append((new_kite, 3))

                        new_kite.vertices = [a0, a1, a2, a3]

                    if kite3 is None:
                        new_kite = Kite()
                        new_kite.draw(dart, 'bottom-right')
                        all_tiles.append(new_kite)

                        # Assign vertices
                        d0, d1, d2, d3 = dart.vertices
                        b0 = d1
                        b1 = vertex_exists(new_kite.vertex_coordinates[1], d1)
                        b2 = vertex_exists(new_kite.vertex_coordinates[2], d2)
                        b3 = d2

                        switch = True if not b1 or not b2 else False

                        if not b1:
                            b1 = Vertex(new_kite.vertex_coordinates[1])
                            all_vertices.append(b1)

                            b0.adjacent_vertices.append(b1)
                            b1.adjacent_vertices.append(b0)

                        if not b2:
                            b2 = Vertex(new_kite.vertex_coordinates[2])
                            all_vertices.append(b2)

                            b2.adjacent_vertices.append(b3)
                            b3.adjacent_vertices.append(b2)

                        if switch:
                            b1.adjacent_vertices.append(b2)
                            b2.adjacent_vertices.append(b1)

                        # Add vertex components
                        b0.vertex_components.append((new_kite, 0))
                        b1.vertex_components.append((new_kite, 1))
                        b2.vertex_components.append((new_kite, 2))
                        b3.vertex_components.append((new_kite, 3))

                        new_kite.vertices = [b0, b1, b2, b3]

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
                        new_dart1 = Dart()
                        new_dart1.draw(left_kite, 'top-left')
                        all_tiles.append(new_dart1)

                        # Assign vertices
                        k0, k1, k2, k3 = left_kite.vertices
                        c0 = vertex_exists(new_dart1.vertex_coordinates[0], k0)
                        c1 = k0
                        c2 = k3
                        c3 = vertex_exists(new_dart1.vertex_coordinates[3], k3)

                        switch = True if not c0 or not c3 else False

                        if not c0:
                            c0 = Vertex(new_dart1.vertex_coordinates[0], [c1])
                            all_vertices.append(c0)
                            c1.adjacent_vertices.append(c0)

                        if not c3:
                            c3 = Vertex(new_dart1.vertex_coordinates[3], [c2])
                            all_vertices.append(c3)
                            c2.adjacent_vertices.append(c3)

                        if switch:
                            c0.adjacent_vertices.append(c3)
                            c3.adjacent_vertices.append(c0)

                        # Add vertex components
                        c0.vertex_components.append((new_dart1, 0))
                        c1.vertex_components.append((new_dart1, 1))
                        c2.vertex_components.append((new_dart1, 2))
                        c3.vertex_components.append((new_dart1, 3))

                        new_dart1.vertices = [c0, c1, c2, c3]

                    if dart3 is None:
                        new_dart3 = Dart()
                        new_dart3.draw(right_kite, 'top-right')
                        all_tiles.append(new_dart3)

                        # Assign vertices
                        k0, k1, k2, k3 = right_kite.vertices
                        d0 = vertex_exists(new_dart3.vertex_coordinates[0], k0)
                        d1 = vertex_exists(new_dart3.vertex_coordinates[1], k1)
                        d2 = k1
                        d3 = k0

                        switch = True if not d0 or not d1 else False

                        if not d0:
                            d0 = Vertex(new_dart3.vertex_coordinates[0])
                            all_vertices.append(d0)

                            d0.adjacent_vertices.append(d3)
                            d3.adjacent_vertices.append(d0)

                        if not d1:
                            d1 = Vertex(new_dart3.vertex_coordinates[1])
                            all_vertices.append(d1)

                            d1.adjacent_vertices.append(d2)
                            d2.adjacent_vertices.append(d1)

                        if switch:
                            d0.adjacent_vertices.append(d1)
                            d1.adjacent_vertices.append(d0)

                        # Add vertex components
                        d0.vertex_components.append((new_dart3, 0))
                        d1.vertex_components.append((new_dart3, 1))
                        d2.vertex_components.append((new_dart3, 2))
                        d3.vertex_components.append((new_dart3, 3))

                        new_dart3.vertices = [d0, d1, d2, d3]

                elif vertex_key == 'star':
                    edge_vertex.name = 'star'

                    darts = []
                    for val in edge_vertex.vertex_components:
                        darts.append(val[0])

                    for dart in darts:
                        if len(dart.vertices[1].vertex_components) == 2:
                            new_dart = Dart()
                            new_dart.draw(dart, 'top-right')
                            all_tiles.append(new_dart)

                            d0, d1, d2, d3 = dart.vertices
                            v0 = d0
                            v1 = vertex_exists(new_dart.vertex_coordinates[1], d0)  # should always exist
                            v2 = vertex_exists(new_dart.vertex_coordinates[2], d1)
                            v3 = d1

                            if not v2:
                                v2 = Vertex(new_dart.vertex_coordinates[2], [v1, v3])
                                all_vertices.append(v2)
                                v1.adjacent_vertices.append(v2)
                                v3.adjacent_vertices.append(v2)

                            # Add vertex components
                            v0.vertex_components.append((new_dart, 0))
                            v1.vertex_components.append((new_dart, 1))
                            v2.vertex_components.append((new_dart, 2))
                            v3.vertex_components.append((new_dart, 3))

                            new_dart.vertices = [v0, v1, v2, v3]

                elif vertex_key == 'sun':
                    edge_vertex.name = 'sun'

                    kites = []
                    for val in edge_vertex.vertex_components:
                        kites.append(val[0])

                    edge_kites = []
                    for adj in edge_vertex.adjacent_vertices:
                        adj_kites = []
                        for comp in adj.vertex_components:
                            if comp[0].name == 'kite':
                                adj_kites.append(comp[0])

                        total = 0
                        for ad in adj_kites:
                            total += kites.count(ad)

                        if total == 1:
                            edge_kites.append(adj_kites[0])  # since there is only one match, it is adj_kites[0]

                            if len(kites) == 3:
                                if adj_kites[0].vertices.index(adj) == 1:
                                    new_kite = Kite()
                                    new_kite.draw(adj_kites[0], 'bottom-right')
                                    all_tiles.append(new_kite)

                                    # Assign vertices
                                    k0, k1, k2, k3 = adj_kites[0].vertices
                                    c0 = vertex_exists(new_kite.vertex_coordinates[0], k1)
                                    c1 = vertex_exists(new_kite.vertex_coordinates[1], k2)
                                    c2 = k2
                                    c3 = k1

                                    switch = True if not c0 or not c1 else False

                                    if not c0:
                                        c0 = Vertex(new_kite.vertex_coordinates[0], [c3])
                                        all_vertices.append(c0)
                                        c3.adjacent_vertices.append(c0)

                                    if not c1:
                                        c1 = Vertex(new_kite.vertex_coordinates[3], [c2])
                                        all_vertices.append(c1)
                                        c2.adjacent_vertices.append(c1)

                                    if switch:
                                        c0.adjacent_vertices.append(c1)
                                        c1.adjacent_vertices.append(c0)

                                    # Add vertex components
                                    c0.vertex_components.append((new_kite, 0))
                                    c1.vertex_components.append((new_kite, 1))
                                    c2.vertex_components.append((new_kite, 2))
                                    c3.vertex_components.append((new_kite, 3))

                                    new_kite.vertices = [c0, c1, c2, c3]

                                elif adj_kites[0].vertices.index(adj) == 3:
                                    new_kite = Kite()
                                    new_kite.draw(adj_kites[0], 'bottom-left')
                                    all_tiles.append(new_kite)

                                    # Assign vertices
                                    k0, k1, k2, k3 = adj_kites[0].vertices
                                    c0 = vertex_exists(new_kite.vertex_coordinates[0], k0)
                                    c1 = k3
                                    c2 = k2
                                    c3 = vertex_exists(new_kite.vertex_coordinates[3], k3)

                                    switch = True if not c0 or not c3 else False

                                    if not c0:
                                        c0 = Vertex(new_kite.vertex_coordinates[0], [c1])
                                        all_vertices.append(c0)
                                        c1.adjacent_vertices.append(c0)

                                    if not c3:
                                        c3 = Vertex(new_kite.vertex_coordinates[3], [c2])
                                        all_vertices.append(c3)
                                        c2.adjacent_vertices.append(c3)

                                    if switch:
                                        c0.adjacent_vertices.append(c3)
                                        c3.adjacent_vertices.append(c0)

                                    # Add vertex components
                                    c0.vertex_components.append((new_kite, 0))
                                    c1.vertex_components.append((new_kite, 1))
                                    c2.vertex_components.append((new_kite, 2))
                                    c3.vertex_components.append((new_kite, 3))

                                    new_kite.vertices = [c0, c1, c2, c3]
                            elif len(kites) == 4:
                                if adj_kites[0].vertices.index(adj) == 1:
                                    new_kite = Kite()
                                    new_kite.draw(adj_kites[0], 'bottom-right')
                                    all_tiles.append(new_kite)

                                    # Assign vertices
                                    k0, k1, k2, k3 = adj_kites[0].vertices
                                    c0 = vertex_exists(new_kite.vertex_coordinates[0], k1)
                                    c1 = vertex_exists(new_kite.vertex_coordinates[1], k2)
                                    c2 = k2
                                    c3 = k1

                                    switch = True if not c0 or not c1 else False

                                    if not c0:
                                        c0 = Vertex(new_kite.vertex_coordinates[0], [c3])
                                        all_vertices.append(c0)
                                        c3.adjacent_vertices.append(c0)

                                    if not c1:
                                        c1 = Vertex(new_kite.vertex_coordinates[3], [c2])
                                        all_vertices.append(c1)
                                        c2.adjacent_vertices.append(c1)

                                    if switch:
                                        c0.adjacent_vertices.append(c1)
                                        c1.adjacent_vertices.append(c0)

                                    # Add vertex components
                                    c0.vertex_components.append((new_kite, 0))
                                    c1.vertex_components.append((new_kite, 1))
                                    c2.vertex_components.append((new_kite, 2))
                                    c3.vertex_components.append((new_kite, 3))

                                    new_kite.vertices = [c0, c1, c2, c3]

                    # print('edge kites', edge_kites)

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
