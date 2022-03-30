from kites_and_darts import Kite, Dart
from vertex import Vertex

dictionary_of_all_unique_possibilities = {(('dart', 2), ): 'ace',
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


def force_tiles(vertices, tiles):

    while True:

        tiles_len = len(tiles)

        edge_vertices = []
        for vertex in vertices:
            if vertex.name == 'edge':
                edge_vertices.append(vertex)

        for edge_vertex in edge_vertices:

            set_ = []
            for vert in edge_vertex.congruent_vertices:
                set_.append((vert[0].name, vert[1]))
            set_.sort()

            vertex_key = dictionary_of_all_unique_possibilities.get(tuple(set_))
            if vertex_key is not None:
                if vertex_key == 'ace':
                    edge_vertex.name = 'ace'
                    dart = None
                    k1, k3 = None, None
                    for val in edge_vertex.congruent_vertices:
                        if val[0].name == 'dart':
                            dart = val[0]
                        elif val[1] == 1:
                            k1 = val[0]
                        else:
                            k3 = val[0]

                    if k1 is None:
                        new_kite = Kite()
                        new_kite.draw(dart, 'bottom-left')
                        update_tiles(new_kite, tiles, vertices, False)
                    if k3 is None:
                        new_kite = Kite()
                        new_kite.draw(dart, 'bottom-right')
                        update_tiles(new_kite, tiles, vertices, False)

                elif vertex_key == 'sun':
                    edge_vertex.name = 'sun'

                    if len(edge_vertex.congruent_vertices) == 5:
                        continue

                    k1, k2, k3, k4 = None, None, None, None
                    for val in edge_vertex.congruent_vertices:
                        if k1 is None:
                            k1 = val[0]
                        else:
                            if k2 is None:
                                k2 = val[0]
                            else:
                                if k3 is None:
                                    k3 = val[0]
                                else:
                                    k4 = val[0]

                    if k4 is None:
                        new_kite1, new_kite2 = Kite(), Kite()
                        # k1, k2, -, -, -
                        if compare_coord(k1.vertices[1], k2.vertices[3]):
                            # k1, k2, k3, -, -
                            if compare_coord(k2.vertices[1], k3.vertices[3]):
                                new_kite1.draw(k1, 'bottom-left')
                                new_kite2.draw(k3, 'bottom-right')
                            # k1, k2, -, -, k3
                            elif compare_coord(k3.vertices[1], k1.vertices[3]):
                                new_kite1.draw(k3, 'bottom-left')
                                new_kite2.draw(k2, 'bottom-right')
                            # k1, k2, -, k3, -
                            else:
                                new_kite1.draw(k1, 'bottom-left')
                                new_kite2.draw(k2, 'bottom-right')
                        # k1, -, -, -, k2
                        elif compare_coord(k2.vertices[1], k1.vertices[3]):
                            # k1, -, -, k3, k2
                            if compare_coord(k3.vertices[1], k2.vertices[3]):
                                new_kite1.draw(k3, 'bottom-left')
                                new_kite2.draw(k1, 'bottom-right')
                            # k1, k3, -, -, k2
                            elif compare_coord(k1.vertices[1], k3.vertices[3]):
                                new_kite1.draw(k2, 'bottom-left')
                                new_kite2.draw(k3, 'bottom-right')
                            # k1, -, k3, -, k2
                            else:
                                new_kite1.draw(k2, 'bottom-left')
                                new_kite2.draw(k1, 'bottom-right')
                        # k1, k3, -, -, -
                        elif compare_coord(k1.vertices[1], k3.vertices[3]):
                            # k1, k3, k2, -, -
                            if compare_coord(k3.vertices[1], k2.vertices[3]):
                                new_kite1.draw(k1, 'bottom-left')
                                new_kite2.draw(k2, 'bottom-right')
                            # k1, k3, -, -, k2
                            elif compare_coord(k2.vertices[1], k1.vertices[3]):
                                new_kite1.draw(k2, 'bottom-left')
                                new_kite2.draw(k3, 'bottom-right')
                            # k1, k3, -, k2, -
                            else:
                                new_kite1.draw(k1, 'bottom-left')
                                new_kite2.draw(k3, 'bottom-right')
                        # k1, -, -, -, k3
                        elif compare_coord(k3.vertices[1], k1.vertices[3]):
                            # k1, k2, -, -, k3
                            if compare_coord(k1.vertices[1], k2.vertices[3]):
                                new_kite1.draw(k3, 'bottom-left')
                                new_kite2.draw(k2, 'bottom-right')
                            # k1, -, -, k2, k3
                            elif compare_coord(k2.vertices[1], k3.vertices[3]):
                                new_kite1.draw(k2, 'bottom-left')
                                new_kite2.draw(k1, 'bottom-right')
                            # k1, -, k2, -, k3
                            else:
                                new_kite1.draw(k3, 'bottom-left')
                                new_kite2.draw(k1, 'bottom-right')
                        if new_kite1.vertices is None or new_kite2.vertices is None:
                            print(edge_vertex.congruent_vertices)
                        update_tiles([new_kite1, new_kite2], tiles, vertices, False)
                    else:
                        new_kite = Kite()
                        # k1, k2, -, -, -
                        if compare_coord(k1.vertices[1], k2.vertices[3]):
                            # k1, k2, k3, -, -
                            if compare_coord(k2.vertices[1], k3.vertices[3]):
                                # k1, k2, k3, k4, -
                                if compare_coord(k3.vertices[1], k4.vertices[3]):
                                    new_kite.draw(k4, 'bottom-right')
                                # k1, k2, k3, -, k4
                                else:
                                    new_kite.draw(k3, 'bottom-right')
                            # k1, k2, -, -, k3
                            elif compare_coord(k3.vertices[1], k1.vertices[3]):
                                # k1, k2, k4, -, k3
                                if compare_coord(k2.vertices[1], k4.vertices[3]):
                                    new_kite.draw(k4, 'bottom-right')
                                # k1, k2, -, k4, k3
                                else:
                                    new_kite.draw(k2, 'bottom-right')
                            # k1, k2, -, k3, -
                            else:
                                # k1, k2, k4, k3, -
                                if compare_coord(k2.vertices[1], k4.vertices[3]):
                                    new_kite.draw(k3, 'bottom-right')
                                # k1, k2, -, k3, k4
                                else:
                                    new_kite.draw(k2, 'bottom-right')
                        # k1, - , -, -, k2
                        elif compare_coord(k2.vertices[1], k1.vertices[3]):
                            # k1, k3, -, -, k2
                            if compare_coord(k1.vertices[1], k3.vertices[3]):
                                # k1, k3, -, k4, k2
                                if compare_coord(k4.vertices[1], k2.vertices[3]):
                                    new_kite.draw(k3, 'bottom-right')
                                # k1, k3, k4, -, k2
                                else:
                                    new_kite.draw(k4, 'bottom-right')
                            # k1, -, -, k3, k2
                            elif compare_coord(k3.vertices[1], k2.vertices[3]):
                                # k1, k4, -, k3, k2
                                if compare_coord(k1.vertices[1], k4.vertices[3]):
                                    new_kite.draw(k4, 'bottom-right')
                                # k1, -, k4, k3, k2
                                else:
                                    new_kite.draw(k1, 'bottom-right')
                            # k1, -, k3, -, k2
                            else:
                                # k1, k4, k3, -, k2
                                if compare_coord(k1.vertices[1], k4.vertices[3]):
                                    new_kite.draw(k3, 'bottom-right')
                                # k1, -, k3, k4, k2
                                else:
                                    new_kite.draw(k1, 'bottom-right')
                        # k1, k3, -, - , -
                        elif compare_coord(k1.vertices[1], k3.vertices[3]):
                            # k1, k3, k2, - , -
                            if compare_coord(k3.vertices[1], k2.vertices[3]):
                                # k1, k3, k2, k4 , -
                                if compare_coord(k2.vertices[1], k4.vertices[3]):
                                    new_kite.draw(k4, 'bottom-right')
                                # k1, k3, k2, - , k4
                                else:
                                    new_kite.draw(k2, 'bottom-right')
                            # k1, k3, -, - , k2
                            elif compare_coord(k2.vertices[1], k1.vertices[3]):
                                # k1, k3, k4, - , k2
                                if compare_coord(k3.vertices[1], k4.vertices[3]):
                                    new_kite.draw(k4, 'bottom-right')
                                # k1, k3, -, k4 , k2
                                else:
                                    new_kite.draw(k3, 'bottom-right')
                            # k1, k3, -, k2 , -
                            else:
                                # k1, k3, k4, k2 , -
                                if compare_coord(k3.vertices[1], k4.vertices[3]):
                                    new_kite.draw(k2, 'bottom-right')
                                # k1, k3, -, k2 , k4
                                else:
                                    new_kite.draw(k3, 'bottom-right')
                        # k1, -, -, -, k3
                        elif compare_coord(k3.vertices[1], k1.vertices[3]):
                            # k1, k2, -, -, k3
                            if compare_coord(k1.vertices[1], k2.vertices[3]):
                                # k1, k2, k4, -, k3
                                if compare_coord(k2.vertices[1], k4.vertices[3]):
                                    new_kite.draw(k4, 'bottom-right')
                                # k1, k2, -, k4, k3
                                else:
                                    new_kite.draw(k2, 'bottom-right')
                            # k1, -, -, k2, k3
                            elif compare_coord(k2.vertices[1], k1.vertices[3]):
                                # k1, k4, -, k2, k3
                                if compare_coord(k1.vertices[1], k4.vertices[3]):
                                    new_kite.draw(k4, 'bottom-right')
                                # k1, -, k4, k2, k3
                                else:
                                    new_kite.draw(k1, 'bottom-right')
                            # k1, -, k2, -, k3
                            else:
                                # k1, k4, k2, -, k3
                                if compare_coord(k1.vertices[1], k4.vertices[3]):
                                    new_kite.draw(k2, 'bottom-right')
                                # k1, -, k2, k4, k3
                                else:
                                    new_kite.draw(k1, 'bottom-right')
                        # k1, k4, -, -, -
                        elif compare_coord(k1.vertices[1], k4.vertices[3]):
                            # k1, k4, k2, -, -
                            if compare_coord(k4.vertices[1], k2.vertices[3]):
                                # k1, k4, k2, k3, -
                                if compare_coord(k2.vertices[1], k3.vertices[3]):
                                    new_kite.draw(k3, 'bottom-right')
                                # k1, k4, k2, -, k3
                                else:
                                    new_kite.draw(k2, 'bottom-right')
                            # k1, k4, -, -, k2
                            elif compare_coord(k2.vertices[1], k1.vertices[3]):
                                # k1, k4, k3, -, k2
                                if compare_coord(k4.vertices[1], k3.vertices[3]):
                                    new_kite.draw(k3, 'bottom-right')
                                # k1, k4, -, k3, k2
                                else:
                                    new_kite.draw(k4, 'bottom-right')
                            # k1, k4, -, k2, -
                            else:
                                # k1, k4, k3, k2, -
                                if compare_coord(k4.vertices[1], k3.vertices[3]):
                                    new_kite.draw(k2, 'bottom-right')
                                # k1, k4, -, k2, k3
                                else:
                                    new_kite.draw(k4, 'bottom-right')
                        # k1, -, -, -, k4
                        elif compare_coord(k4.vertices[1], k1.vertices[3]):
                            # k1, k2, -, -, k4
                            if compare_coord(k1.vertices[1], k2.vertices[3]):
                                # k1, k2, k3, -, k4
                                if compare_coord(k2.vertices[1], k3.vertices[3]):
                                    new_kite.draw(k3, 'bottom-right')
                                # k1, k2, -, k3, k4
                                else:
                                    new_kite.draw(k2, 'bottom-right')
                            # k1, -, -, k2, k4
                            elif compare_coord(k2.vertices[1], k1.vertices[3]):
                                # k1, k3, -, k2, k4
                                if compare_coord(k1.vertices[1], k3.vertices[3]):
                                    new_kite.draw(k3, 'bottom-right')
                                # k1, -, k3, k2, k4
                                else:
                                    new_kite.draw(k1, 'bottom-right')
                            # k1, -, k2, -, k4
                            else:
                                # k1, k3, k2, -, k4
                                if compare_coord(k1.vertices[1], k3.vertices[3]):
                                    new_kite.draw(k2, 'bottom-right')
                                # k1, -, k2, k3, k4
                                else:
                                    new_kite.draw(k1, 'bottom-right')
                        update_tiles(new_kite, tiles, vertices, False)

                elif vertex_key == 'star':
                    edge_vertex.name = 'star'

                    if len(edge_vertex.congruent_vertices) == 5:
                        continue

                    k1, k2, k3, k4 = None, None, None, None
                    for val in edge_vertex.congruent_vertices:
                        if k1 is None:
                            k1 = val[0]
                        else:
                            if k2 is None:
                                k2 = val[0]
                            else:
                                if k3 is None:
                                    k3 = val[0]
                                else:
                                    k4 = val[0]

                    new_kite = Dart()
                    # k1, k2, -, -, -
                    if compare_coord(k1.vertices[1], k2.vertices[3]):
                        # k1, k2, k3, -, -
                        if compare_coord(k2.vertices[1], k3.vertices[3]):
                            # k1, k2, k3, k4, -
                            if compare_coord(k3.vertices[1], k4.vertices[3]):
                                new_kite.draw(k4, 'top-right')
                            # k1, k2, k3, -, k4
                            else:
                                new_kite.draw(k3, 'top-right')
                        # k1, k2, -, -, k3
                        elif compare_coord(k3.vertices[1], k1.vertices[3]):
                            # k1, k2, k4, -, k3
                            if compare_coord(k2.vertices[1], k4.vertices[3]):
                                new_kite.draw(k4, 'top-right')
                            # k1, k2, -, k4, k3
                            else:
                                new_kite.draw(k2, 'top-right')
                        # k1, k2, -, k3, -
                        else:
                            # k1, k2, k4, k3, -
                            if compare_coord(k2.vertices[1], k4.vertices[3]):
                                new_kite.draw(k3, 'top-right')
                            # k1, k2, -, k3, k4
                            else:
                                new_kite.draw(k2, 'top-right')
                    # k1, - , -, -, k2
                    elif compare_coord(k2.vertices[1], k1.vertices[3]):
                        # k1, k3, -, -, k2
                        if compare_coord(k1.vertices[1], k3.vertices[3]):
                            # k1, k3, -, k4, k2
                            if compare_coord(k4.vertices[1], k2.vertices[3]):
                                new_kite.draw(k3, 'top-right')
                            # k1, k3, k4, -, k2
                            else:
                                new_kite.draw(k4, 'top-right')
                        # k1, -, -, k3, k2
                        elif compare_coord(k3.vertices[1], k2.vertices[3]):
                            # k1, k4, -, k3, k2
                            if compare_coord(k1.vertices[1], k4.vertices[3]):
                                new_kite.draw(k4, 'top-right')
                            # k1, -, k4, k3, k2
                            else:
                                new_kite.draw(k1, 'top-right')
                        # k1, -, k3, -, k2
                        else:
                            # k1, k4, k3, -, k2
                            if compare_coord(k1.vertices[1], k4.vertices[3]):
                                new_kite.draw(k3, 'top-right')
                            # k1, -, k3, k4, k2
                            else:
                                new_kite.draw(k1, 'top-right')
                    # k1, k3, -, - , -
                    elif compare_coord(k1.vertices[1], k3.vertices[3]):
                        # k1, k3, k2, - , -
                        if compare_coord(k3.vertices[1], k2.vertices[3]):
                            # k1, k3, k2, k4 , -
                            if compare_coord(k2.vertices[1], k4.vertices[3]):
                                new_kite.draw(k4, 'top-right')
                            # k1, k3, k2, - , k4
                            else:
                                new_kite.draw(k2, 'top-right')
                        # k1, k3, -, - , k2
                        elif compare_coord(k2.vertices[1], k1.vertices[3]):
                            # k1, k3, k4, - , k2
                            if compare_coord(k3.vertices[1], k4.vertices[3]):
                                new_kite.draw(k4, 'top-right')
                            # k1, k3, -, k4 , k2
                            else:
                                new_kite.draw(k3, 'top-right')
                        # k1, k3, -, k2 , -
                        else:
                            # k1, k3, k4, k2 , -
                            if compare_coord(k3.vertices[1], k4.vertices[3]):
                                new_kite.draw(k2, 'top-right')
                            # k1, k3, -, k2 , k4
                            else:
                                new_kite.draw(k3, 'top-right')
                    # k1, -, -, -, k3
                    elif compare_coord(k3.vertices[1], k1.vertices[3]):
                        # k1, k2, -, -, k3
                        if compare_coord(k1.vertices[1], k2.vertices[3]):
                            # k1, k2, k4, -, k3
                            if compare_coord(k2.vertices[1], k4.vertices[3]):
                                new_kite.draw(k4, 'top-right')
                            # k1, k2, -, k4, k3
                            else:
                                new_kite.draw(k2, 'top-right')
                        # k1, -, -, k2, k3
                        elif compare_coord(k2.vertices[1], k1.vertices[3]):
                            # k1, k4, -, k2, k3
                            if compare_coord(k1.vertices[1], k4.vertices[3]):
                                new_kite.draw(k4, 'top-right')
                            # k1, -, k4, k2, k3
                            else:
                                new_kite.draw(k1, 'top-right')
                        # k1, -, k2, -, k3
                        else:
                            # k1, k4, k2, -, k3
                            if compare_coord(k1.vertices[1], k4.vertices[3]):
                                new_kite.draw(k2, 'top-right')
                            # k1, -, k2, k4, k3
                            else:
                                new_kite.draw(k1, 'top-right')
                    # k1, k4, -, -, -
                    elif compare_coord(k1.vertices[1], k4.vertices[3]):
                        # k1, k4, k2, -, -
                        if compare_coord(k4.vertices[1], k2.vertices[3]):
                            # k1, k4, k2, k3, -
                            if compare_coord(k2.vertices[1], k3.vertices[3]):
                                new_kite.draw(k3, 'top-right')
                            # k1, k4, k2, -, k3
                            else:
                                new_kite.draw(k2, 'top-right')
                        # k1, k4, -, -, k2
                        elif compare_coord(k2.vertices[1], k1.vertices[3]):
                            # k1, k4, k3, -, k2
                            if compare_coord(k4.vertices[1], k3.vertices[3]):
                                new_kite.draw(k3, 'top-right')
                            # k1, k4, -, k3, k2
                            else:
                                new_kite.draw(k4, 'top-right')
                        # k1, k4, -, k2, -
                        else:
                            # k1, k4, k3, k2, -
                            if compare_coord(k4.vertices[1], k3.vertices[3]):
                                new_kite.draw(k2, 'top-right')
                            # k1, k4, -, k2, k3
                            else:
                                new_kite.draw(k4, 'top-right')
                    # k1, -, -, -, k4
                    elif compare_coord(k4.vertices[1], k1.vertices[3]):
                        # k1, k2, -, -, k4
                        if compare_coord(k1.vertices[1], k2.vertices[3]):
                            # k1, k2, k3, -, k4
                            if compare_coord(k2.vertices[1], k3.vertices[3]):
                                new_kite.draw(k3, 'top-right')
                            # k1, k2, -, k3, k4
                            else:
                                new_kite.draw(k2, 'top-right')
                        # k1, -, -, k2, k4
                        elif compare_coord(k2.vertices[1], k1.vertices[3]):
                            # k1, k3, -, k2, k4
                            if compare_coord(k1.vertices[1], k3.vertices[3]):
                                new_kite.draw(k3, 'top-right')
                            # k1, -, k3, k2, k4
                            else:
                                new_kite.draw(k1, 'top-right')
                        # k1, -, k2, -, k4
                        else:
                            # k1, k3, k2, -, k4
                            if compare_coord(k1.vertices[1], k3.vertices[3]):
                                new_kite.draw(k2, 'top-right')
                            # k1, -, k2, k3, k4
                            else:
                                new_kite.draw(k1, 'top-right')
                    update_tiles(new_kite, tiles, vertices, False)

                elif vertex_key == 'deuce':
                    edge_vertex.name = 'deuce'
                    k0, kite0 = None, None
                    d1, d3 = None, None
                    for val in edge_vertex.congruent_vertices:
                        if val[0].name == 'kite':
                            if k0 is None:
                                k0 = val[0]
                            else:
                                kite0 = val[0]
                        elif val[1] == 1:
                            d1 = val[0]
                        else:
                            d3 = val[0]

                    if compare_coord(kite0.vertices[1], k0.vertices[3]):
                        k_temp = k0
                        k0 = kite0
                        kite0 = k_temp

                    if d1 is None:
                        new_dart = Dart()
                        new_dart.draw(k0, 'top-left')
                        update_tiles(new_dart, tiles, vertices, False)
                    if d3 is None:
                        new_dart = Dart()
                        new_dart.draw(kite0, 'top-right')
                        update_tiles(new_dart, tiles, vertices, False)

                elif vertex_key == 'jack':
                    edge_vertex.name = 'jack'
                    d1, d3 = None, None
                    k0 = None
                    k2, kite2 = None, None

                    for val in edge_vertex.congruent_vertices:
                        if (val[0].name, val[1]) == ('dart', 1):
                            d1 = val[0]
                        elif (val[0].name, val[1]) == ('dart', 3):
                            d3 = val[0]
                        elif (val[0].name, val[1]) == ('kite', 0):
                            k0 = val[0]
                        else:
                            if k2 is None:
                                k2 = val[0]
                            else:
                                kite2 = val[0]

                    if k0 is None:
                        if d1 is None:
                            new_d1 = Dart()
                            new_k0 = Kite()
                            new_k0.draw(d3, 'bottom-left')
                            new_d1.draw(new_k0, 'top-left')
                            update_tiles([new_d1, new_k0], tiles, vertices, False)
                            d1 = new_d1
                            k0 = new_k0
                        elif d3 is None:
                            new_d3 = Dart()
                            new_k0 = Kite()
                            new_k0.draw(d1, 'bottom-right')
                            new_d3.draw(new_k0, 'top-right')
                            update_tiles([new_d3, new_k0], tiles, vertices, False)
                            d3 = new_d3
                            k0 = new_k0
                        else:
                            new_k0 = Kite()
                            new_k0.draw(d1, 'bottom-right')
                            update_tiles(new_k0, tiles, vertices, False)
                            k0 = new_k0

                    if d1 is None:
                        new_dart = Dart()
                        new_dart.draw(k0, 'top-left')
                        update_tiles(new_dart, tiles, vertices, False)
                        d1 = new_dart
                    if d3 is None:
                        new_dart = Dart()
                        new_dart.draw(k0, 'top-right')
                        update_tiles(new_dart, tiles, vertices, False)
                        d3 = new_dart
                    if kite2 is None:
                        new_kite = Kite()
                        if compare_coord(d1.vertices[0], k2.vertices[3]):
                            new_kite.draw(d3, 'top-left')
                        else:
                            new_kite.draw(d1, 'top-right')
                        update_tiles(new_kite, tiles, vertices, False)

                elif vertex_key == 'queen':
                    edge_vertex.name = 'queen'
                    k1, kite1 = None, None
                    k3, kite3 = None, None
                    d0 = None
                    for val in edge_vertex.congruent_vertices:
                        if (val[0].name, val[1]) == ('kite', 1):
                            if k1 is None:
                                k1 = val[0]
                            else:
                                kite1 = val[0]
                        elif (val[0].name, val[1]) == ('kite', 3):
                            if k3 is None:
                                k3 = val[0]
                            else:
                                kite3 = val[0]
                        else:
                            d0 = val[0]

                    if k1 is None:
                        new_k1, new_kite1 = Kite(), Kite()
                        new_k1.draw(k3, 'top-left')
                        new_kite1.draw(kite3, 'top-left')
                        update_tiles([new_k1, new_kite1], tiles, vertices, False)
                        k1 = new_k1
                        kite1 = new_kite1

                    if k3 is None:
                        new_k3, new_kite3 = Kite(), Kite()
                        new_k3.draw(k1, 'top-right')
                        new_kite3.draw(kite1, 'top-right')
                        update_tiles([new_k3, new_kite3], tiles, vertices, False)
                        k3 = new_k3
                        kite3 = new_kite3

                    if kite1 is None:
                        new_kite = Kite()
                        if compare_coord(k1.vertices[0], k3.vertices[0]):
                            new_kite.draw(kite3, 'top-left')
                        else:
                            new_kite.draw(k3, 'top-left')
                        update_tiles(new_kite, tiles, vertices, False)
                        kite1 = new_kite

                    if kite3 is None:
                        new_kite = Kite()
                        if compare_coord(k1.vertices[0], k3.vertices[0]):
                            new_kite.draw(kite1, 'top-right')
                        else:
                            new_kite.draw(k1, 'top-right')
                        update_tiles(new_kite, tiles, vertices, False)
                        kite3 = new_kite

                    if d0 is None:
                        new_dart = Dart()
                        if compare_coord(k1.vertices[0], k3.vertices[0]):
                            if compare_coord(k1.vertices[2], kite3.vertices[2]):
                                new_dart.draw(k3, 'bottom-left')
                            else:
                                new_dart.draw(k1, 'bottom-right')
                        else:
                            if compare_coord(k1.vertices[2], k3.vertices[2]):
                                new_dart.draw(kite3, 'bottom-left')
                            else:
                                new_dart.draw(k1, 'bottom-right')
                        update_tiles(new_dart, tiles, vertices, False)

                elif vertex_key == 'king':
                    edge_vertex.name = 'king'
                    k1, k3 = None, None
                    d1, d2, d3 = None, None, None
                    for val in edge_vertex.congruent_vertices:
                        if (val[0].name, val[1]) == ('kite', 1):
                            k1 = val[0]
                        elif (val[0].name, val[1]) == ('kite', 3):
                            k3 = val[0]
                        else:
                            if d1 is None:
                                d1 = val[0]
                            else:
                                if d2 is None:
                                    d2 = val[0]
                                else:
                                    d3 = val[0]

                    if k1 is None:
                        new_kite = Kite()
                        new_kite.draw(k3, 'top-left')
                        update_tiles(new_kite, tiles, vertices, False)
                        k1 = new_kite
                    elif k3 is None:
                        new_kite = Kite()
                        new_kite.draw(k1, 'top-right')
                        update_tiles(new_kite, tiles, vertices, False)

                    if d3 is None:
                        new_dart = Dart()
                        if compare_coord(d1.vertices[1], d2.vertices[3]):
                            if compare_coord(d1.vertices[3], k1.vertices[2]):
                                new_dart.draw(d2, 'top-right')
                            else:
                                new_dart.draw(d1, 'top-left')
                        elif compare_coord(d1.vertices[3], d2.vertices[1]):
                            if compare_coord(d2.vertices[3], k1.vertices[2]):
                                new_dart.draw(d1, 'top-right')
                            else:
                                new_dart.draw(d2, 'top-left')
                        else:
                            if compare_coord(d1.vertices[3], k1.vertices[2]):
                                new_dart.draw(d1, 'top-right')
                            else:
                                new_dart.draw(d2, 'top-right')
                        update_tiles(new_dart, tiles, vertices, False)

                elif vertex_key == 'prince':
                    new_tile = Kite()
                    for val in edge_vertex.congruent_vertices:
                        if (val[0].name, val[1]) == ('kite', 1):
                            new_tile.draw(val[0], 'top-right')
                        elif (val[0].name, val[1]) == ('kite', 3):
                            new_tile.draw(val[0], 'top-left')
                    update_tiles(new_tile, tiles, vertices, False)

                elif vertex_key == 'deuce-jack':
                    d1, d3 = None, None
                    k0 = None
                    for val in edge_vertex.congruent_vertices:
                        if (val[0].name, val[1]) == ('dart', 1):
                            d1 = val[0]
                        elif (val[0].name, val[1]) == ('dart', 3):
                            d3 = val[0]
                        else:
                            k0 = val[0]

                    # (('dart', 1), ('dart', 3), ('kite', 0)): 'deuce-jack'

                    if compare_coord(d1.vertices[0], d3.vertices[0]):
                        edge_vertex.name = 'deuce'
                        new_kite = Kite()
                        if compare_coord(k0.vertices[3], d1.vertices[2]):
                            new_kite.draw(k0, 'top-right')
                        else:
                            new_kite.draw(k0, 'top-left')
                        update_tiles(new_kite, tiles, vertices, False)

                    else:
                        edge_vertex.name = 'jack'
                        new_kite_left = Kite()
                        new_kite_right = Kite()
                        new_kite_left.draw(d1, 'top-right')
                        new_kite_right.draw(d3, 'top-left')
                        update_tiles([new_kite_left, new_kite_right], tiles, vertices, False)

                elif vertex_key == 'king-queen':
                    k1, k3 = None, None
                    d0 = None
                    for val in edge_vertex.congruent_vertices:
                        if (val[0].name, val[1]) == ('kite', 1):
                            k1 = val[0]
                        elif (val[0].name, val[1]) == ('kite', 3):
                            k3 = val[0]
                        else:
                            d0 = val[0]

                    if compare_coord(k1.vertices[2], d0.vertices[3]) and compare_coord(k3.vertices[2], d0.vertices[1]):
                        edge_vertex.name = 'queen'
                        new_left_kite = Kite()
                        new_right_kite = Kite()
                        new_left_kite.draw(k1, 'top-right')
                        new_right_kite.draw(k3, 'top-left')
                        update_tiles([new_left_kite, new_right_kite], tiles, vertices, False)

                else:
                    print('error:', vertex_key)

        if tiles_len == len(tiles):
            break


# ------------------ Helper functions ------------------

# Because of the floating point rounding error, coordinates need to be compared with a tolerance.
# default: 0.001 error tolerance with 6 point rounding accuracy
def compare_coord(first, other):
    value = (first[0] - other[0]) + (first[1] - other[1])
    if abs(value) < 0.001:
        return True
    return False


# Run time for all update functions: O(n^2), where n is len(all_tiles)

# Function: 4 tile vertices loop through all vertices comparing coordinates
# Run Time: O(n): 4n
def update_vertices(tile, all_vertices):

    # update the list of all vertices
    for tile_vertex in tile.vertices:
        # if the tile's vertices do not exist in the list of all vertices, then add it to the list.
        if not any(compare_coord(vertex.coordinates, tile_vertex) for vertex in all_vertices):
            new_vertex = Vertex(tile, tile_vertex)
            all_vertices.append(new_vertex)
            update_congruency(new_vertex, tile)
        else:
            # if it does exist, then update the existing vertex's congruency.
            vert = [vertex for vertex in all_vertices if compare_coord(vertex.coordinates, tile_vertex)]
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
# function will traverse all_tiles.
# Run Time: O(n)
def update_tiles(tiles, all_tiles, all_vertices, check=True):
    # update the list of all tiles
    if isinstance(tiles, list):
        if check:
            for t in tiles:
                flag = 1
                for s in all_tiles:
                    if s == t:
                        flag = 0
                        break
                if flag:
                    update_vertices(t, all_vertices)
                    all_tiles.append(t)
        else:
            for t in tiles:
                update_vertices(t, all_vertices)
                all_tiles.append(t)

    else:
        if check:
            if not (tiles in all_tiles):
                update_vertices(tiles, all_vertices)
                all_tiles.append(tiles)
        else:
            update_vertices(tiles, all_vertices)
            all_tiles.append(tiles)
