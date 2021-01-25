from tiles import Tile


def force_tiles(dictionary, list_of_all_tiles):
    total = dictionary.copy()
    for key, value in total.items():
        vertex_tiles = []
        for val in value:
            vertex_tiles.append((val[0].name, val[1]))  # (tile's name, tile's vertex contained in the key) ex. ('kite' ,0)
        vertex_tiles = sorted(vertex_tiles)

        ace(vertex_tiles, value, dictionary, list_of_all_tiles)
        sun(vertex_tiles, value, dictionary, list_of_all_tiles)
        star(vertex_tiles, value, dictionary, list_of_all_tiles)
        deuce(vertex_tiles, value, dictionary, list_of_all_tiles)
        jack(vertex_tiles, value, dictionary, list_of_all_tiles)
        queen(vertex_tiles, value, dictionary, list_of_all_tiles)

        prince(vertex_tiles, value, dictionary, list_of_all_tiles)
        king(vertex_tiles, value, dictionary, list_of_all_tiles)
    if not (total == dictionary):
        force_tiles(dictionary, list_of_all_tiles)


def ace(vertex_components, vertex_values, dictionary, list_tiles):
    if ('dart', 2) in vertex_components:
        dart = None
        for val in vertex_values:
            if val[0].name == 'dart':
                dart = val[0]

        right_kite = Tile('kite')
        right_kite.draw_kite(dart, 'bottom-left')
        if not check_if_tile_exists(right_kite, list_tiles):
            list_tiles.append(right_kite)
            update_dictionary(dictionary, right_kite)

        left_kite = Tile('kite')
        left_kite.draw_kite(dart, 'bottom-right')
        if not check_if_tile_exists(left_kite, list_tiles):
            list_tiles.append(left_kite)
            update_dictionary(dictionary, left_kite)
        return True
    return False


def sun(vertex_components, vertex_values, dictionary, list_tiles):
    if vertex_components.count(('kite', 2)) == 4:
        new_tile = Tile('kite')
        for val in vertex_values:
            new_tile.draw_kite(val[0], 'bottom-right')
            if not check_if_tile_exists(new_tile, list_tiles):
                list_tiles.append(new_tile)
                update_dictionary(dictionary, new_tile)
                return True
    elif vertex_components.count(('kite', 2)) == 3:
        total = 0
        for val in vertex_values:
            new_tile_right = Tile('kite')
            new_tile_left = Tile('kite')

            new_tile_right.draw_kite(val[0], 'bottom-right')
            if not check_if_tile_exists(new_tile_right, list_tiles):
                list_tiles.append(new_tile_right)
                update_dictionary(dictionary, new_tile_right)
                total += 1

            new_tile_left.draw_kite(val[0], 'bottom-left')
            if not check_if_tile_exists(new_tile_left, list_tiles):
                list_tiles.append(new_tile_left)
                update_dictionary(dictionary, new_tile_left)
                total += 1

            if total >= 2:
                return True
    return False


def star(vertex_components, vertex_values, dictionary, list_tiles):
    if sorted([('dart', 0), ('dart', 0), ('dart', 0), ('dart', 0)]) == vertex_components:
        new_tile = Tile('dart')
        for val in vertex_values:
            new_tile.draw_dart(val[0], 'top-right')
            if not check_if_tile_exists(new_tile, list_tiles):
                list_tiles.append(new_tile)
                update_dictionary(dictionary, new_tile)
                return True
    return False


def deuce(vertex_components, vertex_values, dictionary, list_tiles):
    if vertex_components.count(('kite', 0)) == 2:
        kite1, kite2 = None, None
        for val in vertex_values:
            if val[0].name == 'kite':
                if kite1 is None:
                    kite1 = val[0]
                else:
                    kite2 = val[0]

        new_left_dart = Tile('dart')
        new_right_dart = Tile('dart')
        if kite1.vertices[1] == kite2.vertices[3]:
            new_left_dart.draw_dart(kite1, 'top-left')
            new_right_dart.draw_dart(kite2, 'top-right')
        else:
            new_left_dart.draw_dart(kite1, 'top-right')
            new_right_dart.draw_dart(kite2, 'top-left')

        if not check_if_tile_exists(new_left_dart, list_tiles):
            list_tiles.append(new_left_dart)
            update_dictionary(dictionary, new_left_dart)
        if not check_if_tile_exists(new_right_dart, list_tiles):
            list_tiles.append(new_right_dart)
            update_dictionary(dictionary, new_right_dart)
        return True
    return False


def jack(vertex_components, vertex_values, dictionary, list_tiles):
    total = vertex_components.count(('dart', 1)) + vertex_components.count(('dart', 3))
    if total == 1 and ('kite', 2) in vertex_components and ('dart', 1) in vertex_components:
        dart = None
        for val in vertex_values:
            if val[0].name == 'dart':
                dart = val[0]

        bottom_kite = Tile('kite')
        new_dart = Tile('dart')
        top_left_kite = Tile('kite')
        top_right_kite = Tile('kite')

        bottom_kite.draw_kite(dart, 'bottom-right')
        new_dart.draw_dart(bottom_kite, 'top-right')
        top_left_kite.draw_kite(dart, 'top-right')
        top_right_kite.draw_kite(top_left_kite, 'bottom-right')

        if not check_if_tile_exists(bottom_kite, list_tiles):
            list_tiles.append(bottom_kite)
            update_dictionary(dictionary, bottom_kite)
        if not check_if_tile_exists(new_dart, list_tiles):
            list_tiles.append(new_dart)
            update_dictionary(dictionary, new_dart)

        if not check_if_tile_exists(top_left_kite, list_tiles):
            list_tiles.append(top_left_kite)
            update_dictionary(dictionary, top_left_kite)
        if not check_if_tile_exists(top_right_kite, list_tiles):
            list_tiles.append(top_right_kite)
            update_dictionary(dictionary, top_right_kite)
        return True
    elif total == 1 and ('kite', 2) in vertex_components and ('dart', 3) in vertex_components:
        dart = vertex_values[0][0]
        for val in vertex_values:
            if val[0].name == 'dart':
                dart = val[0]

        top_left_kite = Tile('kite')
        top_right_kite = Tile('kite')
        bottom_kite = Tile('kite')
        new_dart = Tile('dart')

        top_right_kite.draw_kite(dart, 'top-left')
        top_left_kite.draw_kite(top_right_kite, 'bottom-left')
        bottom_kite.draw_kite(dart, 'bottom-left')
        new_dart.draw_dart(bottom_kite, 'top-left')

        if not check_if_tile_exists(top_left_kite, list_tiles):
            list_tiles.append(top_left_kite)
            update_dictionary(dictionary, top_left_kite)
        if not check_if_tile_exists(top_right_kite, list_tiles):
            list_tiles.append(top_right_kite)
            update_dictionary(dictionary, top_right_kite)
        if not check_if_tile_exists(bottom_kite, list_tiles):
            list_tiles.append(bottom_kite)
            update_dictionary(dictionary, bottom_kite)
        if not check_if_tile_exists(new_dart, list_tiles):
            list_tiles.append(new_dart)
            update_dictionary(dictionary, new_dart)
        return True
    elif ('dart', 1) in vertex_components and ('dart', 3) in vertex_components:
        left_dart, right_dart = None, None
        for val in vertex_values:
            if val[0].name == 'dart':
                if val[1] == 1:
                    left_dart = val[0]
                elif val[1] == 3:
                    right_dart = val[0]

        if left_dart.vertices[0] == right_dart.vertices[0]:
            return
        top_left_kite = Tile('kite')
        top_right_kite = Tile('kite')
        bottom_kite = Tile('kite')

        top_left_kite.draw_kite(left_dart, 'top-right')
        top_right_kite.draw_kite(right_dart, 'top-left')
        bottom_kite.draw_kite(left_dart, 'bottom-right')

        if not check_if_tile_exists(top_left_kite, list_tiles):
            list_tiles.append(top_left_kite)
            update_dictionary(dictionary, top_left_kite)

        if not check_if_tile_exists(top_right_kite, list_tiles):
            list_tiles.append(top_right_kite)
            update_dictionary(dictionary, top_right_kite)

        if not check_if_tile_exists(bottom_kite, list_tiles):
            list_tiles.append(bottom_kite)
            update_dictionary(dictionary, bottom_kite)
        return True
    return False


def queen(vertex_components, vertex_values, dictionary, list_tiles):
    if vertex_components.count(('dart', 0)) == 1:
        left_kite = Tile('kite')
        right_kite = Tile('kite')
        dart = None
        for val in vertex_values:
            if val[0].name == 'dart':
                dart = val[0]

        left_kite.draw_kite(dart, 'top-left')
        right_kite.draw_kite(dart, 'top-right')

        if check_if_tile_exists(left_kite, list_tiles) and check_if_tile_exists(right_kite, list_tiles):
            top_right_kite = Tile('kite')
            top_left_kite = Tile('kite')

            top_right_kite.draw_kite(right_kite, 'top-left')
            top_left_kite.draw_kite(left_kite, 'top-right')

            if not check_if_tile_exists(top_right_kite, list_tiles):
                list_tiles.append(top_right_kite)
                update_dictionary(dictionary, top_right_kite)

            if not check_if_tile_exists(top_left_kite, list_tiles):
                list_tiles.append(top_left_kite)
                update_dictionary(dictionary, top_left_kite)
    if vertex_components.count(('kite', 1)) + vertex_components.count(('kite', 3)) == 3:
        if vertex_components.count(('kite', 1)) == 2:
            v1_kite1, v1_kite2, v3_kite3 = None, None, None
            for val in vertex_values:
                if val[0].name == 'kite' and val[1] == 1:
                    if v1_kite1 is None:
                        v1_kite1 = val[0]
                    else:
                        v1_kite2 = val[0]
                elif val[0].name == 'kite' and val[1] == 3:
                    v3_kite3 = val[0]

            temp_kite = Tile('kite')
            new_dart = Tile('dart')
            new_kite = Tile('kite')
            if v3_kite3.vertices[2] == v1_kite1.vertices[2] or v3_kite3.vertices[2] == v1_kite2.vertices[2]:
                # top left
                temp_kite.draw_kite(v3_kite3, 'top-left')
                new_dart.draw_dart(temp_kite, 'bottom-right')
                new_kite.draw_kite(new_dart, 'top-right')
            else:
                # bottom right
                new_dart.draw_dart(v3_kite3, 'bottom-left')
                temp_kite.draw_kite(new_dart, 'top-left')
                new_kite.draw_kite(temp_kite, 'top-right')

            if not check_if_tile_exists(new_dart, list_tiles):
                list_tiles.append(new_dart)
                update_dictionary(dictionary, new_dart)
            if not check_if_tile_exists(new_kite, list_tiles):
                list_tiles.append(new_kite)
                update_dictionary(dictionary, new_kite)
            return True
        elif vertex_components.count(('kite', 3)) == 2:
            v3_kite1, v3_kite2, v1_kite3 = None, None, None
            for val in vertex_values:
                if val[0].name == 'kite' and val[1] == 3:
                    if v3_kite1 is None:
                        v3_kite1 = val[0]
                    else:
                        v3_kite2 = val[0]
                elif val[0].name == 'kite' and val[1] == 1:
                    v1_kite3 = val[0]

            temp_kite = Tile('kite')
            new_dart = Tile('dart')
            new_kite = Tile('kite')
            if v1_kite3.vertices[2] == v3_kite1.vertices[2] or v1_kite3.vertices[2] == v3_kite2.vertices[2]:
                # top left
                temp_kite.draw_kite(v1_kite3, 'top-right')
                new_dart.draw_dart(temp_kite, 'bottom-left')
                new_kite.draw_kite(new_dart, 'top-left')
            else:
                # bottom right
                new_dart.draw_dart(v1_kite3, 'bottom-right')
                temp_kite.draw_kite(new_dart, 'top-right')
                new_kite.draw_kite(temp_kite, 'top-left')

            if not check_if_tile_exists(new_dart, list_tiles):
                list_tiles.append(new_dart)
                update_dictionary(dictionary, new_dart)
            if not check_if_tile_exists(new_kite, list_tiles):
                list_tiles.append(new_kite)
                update_dictionary(dictionary, new_kite)
            return True
    return False


def prince(vertex_components, vertex_values, dictionary, list_tiles):
    # A prince vertex has forced tiles, but is only partially completed. It consists of 1 dart and 2 kites.
    # Depending on which tile is placed next, the prince vertex will either become a King vertex or a Queen vertex.

    if sorted([('dart', 0), ('kite', 1)]) == vertex_components or sorted([('dart', 0), ('kite', 3)]) == vertex_components:
        dart, kite = vertex_values[0][0], vertex_values[1][0]
        if dart.name == 'kite':
            dart, kite = vertex_values[1][0], vertex_values[0][0]

        new_kite = Tile('kite')
        if dart.vertices[1] == kite.vertices[2]:
            new_kite.draw_kite(kite, 'top-left')
            if not check_if_tile_exists(new_kite, list_tiles):
                list_tiles.append(new_kite)
                update_dictionary(dictionary, new_kite)
                return True
        elif dart.vertices[3] == kite.vertices[2]:
            new_kite.draw_kite(kite, 'top-right')
            if not check_if_tile_exists(new_kite, list_tiles):
                list_tiles.append(new_kite)
                update_dictionary(dictionary, new_kite)
                return True
    return False


def king(vertex_components, vertex_values, dictionary, list_tiles):
    if vertex_components.count(('dart', 0)) >= 2 and (('kite', 1) in vertex_components or ('kite', 3) in vertex_components):
        kite_v1, kite_v3 = None, None
        for val in vertex_values:
            if val[0].name == 'kite' and val[1] == 1:
                kite_v1 = val[0]
                break
            if val[0].name == 'kite' and val[1] == 3:
                kite_v3 = val[0]
                break

        if kite_v1 is not None:
            kite = Tile('kite')
            dart1, dart2, dart3 = Tile('dart'), Tile('dart'), Tile('dart')

            kite.draw_kite(kite_v1, 'top-right')
            dart1.draw_dart(kite_v1, 'bottom-right')
            dart2.draw_dart(dart1, 'top-right')
            dart3.draw_dart(dart2, 'top-right')

            if not check_if_tile_exists(kite, list_tiles):
                list_tiles.append(kite)
                update_dictionary(dictionary, kite)
            if not check_if_tile_exists(dart1, list_tiles):
                list_tiles.append(dart1)
                update_dictionary(dictionary, dart1)
            if not check_if_tile_exists(dart2, list_tiles):
                list_tiles.append(dart2)
                update_dictionary(dictionary, dart2)
            if not check_if_tile_exists(dart3, list_tiles):
                list_tiles.append(dart3)
                update_dictionary(dictionary, dart3)
        else:
            kite = Tile('kite')
            dart1, dart2, dart3 = Tile('dart'), Tile('dart'), Tile('dart')

            kite.draw_kite(kite_v3, 'top-left')
            dart1.draw_dart(kite_v3, 'bottom-left')
            dart2.draw_dart(dart1, 'top-left')
            dart3.draw_dart(dart2, 'top-left')

            if not check_if_tile_exists(kite, list_tiles):
                list_tiles.append(kite)
                update_dictionary(dictionary, kite)
            if not check_if_tile_exists(dart1, list_tiles):
                list_tiles.append(dart1)
                update_dictionary(dictionary, dart1)
            if not check_if_tile_exists(dart2, list_tiles):
                list_tiles.append(dart2)
                update_dictionary(dictionary, dart2)
            if not check_if_tile_exists(dart3, list_tiles):
                list_tiles.append(dart3)
                update_dictionary(dictionary, dart3)
        return True
    return False


def check_if_tile_exists(tile, list_of_all_tiles):
    return any(other_tile.vertices == tile.vertices for other_tile in list_of_all_tiles)


def update_dictionary(dictionary, new_tile):
    for index, vertex in enumerate(new_tile.vertices):
        if dictionary.get(vertex) is None:
            dictionary[vertex] = [(new_tile, index)]
        else:
            if not (any(other_tiles == (new_tile, index) for other_tiles in dictionary[vertex])):
                dictionary[vertex].append((new_tile, index))

    # The problem is when the dictionary is updated it traverses every tile and creates a new entry for every vertex
    # that does exists in the dictionary already. Then down below, the optimizer removes all vertex dictionary entries
    # that conform to the requirements. So the dictionary is constantly being built and torn apart every time this
    # function is called.
    # Solution: traverse only the new tile and add them to the dictionary rather than traversing all tiles

    temp = dictionary.copy()
    for key, value in temp.items():
        if len(value) == 5:
            dictionary.pop(key, None)
        elif len(value) == 3 or len(value) == 4:
            bacon = []
            for i in value:
                bacon.append((i[0].name, i[1]))
            if sorted([('dart', 2), ('kite', 1), ('kite', 3)]) == sorted(bacon):
                dictionary.pop(key, None)
            elif sorted([('dart', 1), ('dart', 3), ('kite', 0), ('kite', 0)]) == sorted(bacon):
                dictionary.pop(key, None)

