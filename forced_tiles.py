from tiles import Tile

def update_dictionary(dictionary, list_of_all_tiles):
    for tile in list_of_all_tiles:
        for index, vertex in enumerate(tile.vertices):
            if dictionary.get(vertex) is None:
                dictionary[vertex] = [(tile, index)]
            else:
                if not (any(other_tiles == (tile, index) for other_tiles in dictionary[vertex])):
                    dictionary[vertex].append((tile, index))


def ace(key, dictionary_value, list_of_all_tiles, dictionary):

    vertex = []
    for value in dictionary_value:
        vertex.append((value[0].name, value[1]))



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


def force_tiles_new(dictionary, list_of_all_tiles):
    total = dictionary.copy()
    for key, value in total.items():
        ace(key, value, list_of_all_tiles, dictionary)

        update_dictionary(dictionary, list_of_all_tiles)
    if not (total == dictionary):
        force_tiles_new(dictionary, list_of_all_tiles)