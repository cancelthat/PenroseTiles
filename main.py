import pygame
import math
import time
from tiles import Tile
from dart import Dart
from kite import Kite
from vertex import Vertex
from forced_tiles_recursive_functions import new_force, update_vertices

# Initializer
pygame.init()

# Display Dimensions
UNIT_LENGTH = 28
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 750
DISPLAY = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

# Window Icon
pygame.display.set_caption('Penrose Tiles')
icon = pygame.image.load('pentagon.png')
pygame.display.set_icon(icon)

# Switches
game_is_running = True
kite_is_selected = True
dark_mode = False
build_animation = False

# Information Holders
all_tiles = []
temp_tile = []
tiles_generated = 1
vertex_list = []

# --- Currently Working On ---
# Faster
# Idea: Besides checking the entire list to see if a vertex exists, I can load the vertices into a dictionary and then
# I would only have to check if the key exists.


def show_stats(amount):
    print('vertices: ', len(vertex_list))
    print('tiles generated: ', len(all_tiles) - amount)
    print('total tiles: ', len(all_tiles))
    print('------------------------------------------')
    v0, v1, v2, v3 = all_tiles[0].vertices
    if all_tiles[0].name == 'kite':
        print('std_len: ', distance_formula(v0, v1))
    else:
        print('std_len: ', distance_formula(v1, v2))
    return len(all_tiles)


def distance_formula(val1, val2):
    return round(math.sqrt(pow(val1[0] - val2[0], 2) + pow(val1[1] - val2[1], 2)), 4)


def distance_from_tile_to_point(given_tile, point):
    total = 0
    for vertex in given_tile.vertices:
        total += distance_formula(vertex, point)
    return total


def find_closest_tile(tiles, point):
    shortest_distance = math.inf
    closest_tile = None
    for t in tiles:
        dist = distance_from_tile_to_point(t, point)
        if dist < shortest_distance:
            shortest_distance = dist
            closest_tile = t
    return closest_tile


def find_closest_vertex(given_tile, point):
    v0, v1, v2, v3 = given_tile.vertices

    vertical = 'top'
    horizontal = 'right'
    if distance_formula(v1, point) >= distance_formula(v3, point):
        horizontal = 'left'
    if distance_formula(v0, point) >= distance_formula(v2, point):
        vertical = 'bottom'
    return vertical + '-' + horizontal


def create_new_tile(tiles, click):
    mouse = pygame.mouse.get_pos()
    closest_tile = find_closest_tile(tiles, mouse)
    direction = find_closest_vertex(closest_tile, mouse)

    if click == 1:
        if kite_is_selected:
            new_tile = Kite()
        else:
            new_tile = Dart()
    elif click == 3:
        new_tile = Dart()
    else:
        if kite_is_selected:
            new_tile = Kite()
        else:
            new_tile = Dart()

    new_tile.draw(closest_tile, direction)
    # Check if a tile exists with matching center
    if any(other_tile.center == new_tile.center for other_tile in tiles):
        return None
    return new_tile


#
# -------------- Pre-Game Initialization ----------------
#
initial_tile = Kite()
initial_tile.initial_shape((DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2), unit_length=UNIT_LENGTH)
all_tiles.append(initial_tile)
for vertex_coordinates in initial_tile.vertices:
    vertex_list.append(Vertex(initial_tile, vertex_coordinates))
#
# -------------- Game Loop ----------------
#
while game_is_running:

    # Background color
    DISPLAY.fill((0, 0, 0))
    # Event handler
    for event in pygame.event.get():
        # Exit
        if event.type == pygame.QUIT:
            game_is_running = False

        if event.type == pygame.MOUSEMOTION:
            temp_tile = []
            created_tile = create_new_tile(all_tiles, event.buttons)
            temp_tile.append(created_tile)
        if event.type == pygame.MOUSEBUTTONUP:
            created_tile = create_new_tile(all_tiles, event.button)
            if created_tile is None:
                print('tile already exists')
            else:

                start = time.time()
                edge_vertices = []
                for vertex in vertex_list:
                    if vertex.name == 'edge':
                        edge_vertices.append(vertex)

                all_tiles.append(created_tile)
                update_vertices(created_tile, vertex_list)
                new_force(vertex_list, all_tiles)
                end = time.time()
                print('build time: ', round(end - start, 4), 'sec')
                tiles_generated = show_stats(tiles_generated)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                print('Next shape: dart') if kite_is_selected else print('Next shape: kite')
                kite_is_selected = not kite_is_selected
            elif event.key == pygame.K_k:  # wire-frame
                dark_mode = not dark_mode
            elif event.key == pygame.K_t:
                print('debug')
                new_force(vertex_list, all_tiles)
            elif event.key == pygame.K_q:
                game_is_running = False
            elif event.key == pygame.K_l:  # new random colors
                for t in all_tiles:
                    t.set_random_color()
            elif event.key == pygame.K_r:  # reset
                all_tiles = [initial_tile]
                vertex_list = []
                update_vertices(vertex_list, initial_tile)
            elif event.key == pygame.K_b:  # build animation
                build_animation = True
            elif event.key == pygame.K_c:  # color current tiles
                for tile in all_tiles:
                    tile.set_random_color()
            elif event.key == pygame.K_w:  # color current tiles
                for tile in all_tiles:
                    tile.color = (0, 0, 0)
            elif event.key == pygame.K_1:  # color current tiles
                for vertex in vertex_list:
                    if vertex.name == 'star':
                        for val in vertex.congruent_vertices:
                            fail = val[0]
                            fail.set_random_color()
            elif event.key == pygame.K_2:  # color current tiles
                for vertex in vertex_list:
                    if vertex.name == 'sun':
                        for val in vertex.congruent_vertices:
                            fail = val[0]
                            fail.set_random_color()
            elif event.key == pygame.K_3:  # color current tiles
                for vertex in vertex_list:
                    if vertex.name == 'jack':
                        for val in vertex.congruent_vertices:
                            fail = val[0]
                            fail.set_random_color()
            elif event.key == pygame.K_4:  # color current tiles
                for vertex in vertex_list:
                    if vertex.name == 'queen':
                        for val in vertex.congruent_vertices:
                            fail = val[0]
                            fail.set_random_color()
            elif event.key == pygame.K_5:  # color current tiles
                for vertex in vertex_list:
                    if vertex.name == 'king':
                        for val in vertex.congruent_vertices:
                            fail = val[0]
                            fail.set_random_color()

        if build_animation:
            for bacon in range(1, len(all_tiles) + 1):
                for index, eggs in enumerate(all_tiles[:bacon]):
                    if dark_mode:
                        pygame.draw.polygon(DISPLAY, eggs.color, eggs.vertices, width=0)
                    else:
                        pygame.draw.polygon(DISPLAY, eggs.color, eggs.vertices, width=2)
                pygame.display.update()

                build_time = 70
                if build_time == 0:
                    build_time = 1
                pygame.time.wait(build_time)
            build_animation = False
        elif dark_mode:
            for index, eggs in enumerate(all_tiles):
                pygame.draw.polygon(DISPLAY, eggs.color, eggs.vertices, width=0)
                if temp_tile:
                    if temp_tile[0] is not None:
                        pygame.draw.polygon(DISPLAY, (255, 255, 255), temp_tile[0].vertices, width=0)
        else:
            for index, eggs in enumerate(all_tiles):
                pygame.draw.polygon(DISPLAY, eggs.color, eggs.vertices, width=2)
            if temp_tile:
                if temp_tile[0] is not None:
                    pygame.draw.polygon(DISPLAY, (255, 255, 255), temp_tile[0].vertices, width=2)
        pygame.display.update()
