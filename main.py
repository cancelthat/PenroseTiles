import pygame
import math
import time

from kites_and_darts import Kite, Dart
from vertex import Vertex
from forced_tiles_recursive_functions import force_tiles, update_vertices, update_tiles, compare_coord

# Initializer
pygame.init()

# Adjustable Variables
initial_tile = Kite()
UNIT_LENGTH = 20
displacement_amount = 25

# Display Dimensions
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
wire_frame_active = False
build_animation_active = False
build_animation_active_reverse = False
guide_tile_active = True
prince_vertex_active = False

# Information Holders
all_tiles = []
all_vertices = []
guide_tile = []
tiles_generated = 1

# random note: Kings, stars, and sun don't overlap

# ------------------ to-do ------------------
# Make the prince vertex optional
# Do some renaming
# remap keys
# switch force_tiles(vertices, tiles) to force_tiles(tiles, vertices)
# make dictionary key hashable
# rounding error when std_length is small
# deflate suns
# deflate tiles on top of current tiles


def show_stats(amount):
    total = 0
    for vert in all_vertices:
        if vert.name == 'edge':
            total += 1

    print('------------------------------------------')
    print('vertices: ', len(all_vertices))
    print('edge vertices: ', total)
    print('tiles generated: ', len(all_tiles) - amount)
    print('total tiles: ', len(all_tiles))

    if all_tiles:
        v0, v1, v2, v3 = all_tiles[0].vertices
    else:
        return 0
    if all_tiles[0].name == 'kite':
        print('std_len: ', distance_formula(v0, v1))
    else:
        print('std_len: ', distance_formula(v1, v2))
    return len(all_tiles)


def distance_formula(val1, val2):
    return round(math.sqrt(pow(val1[0] - val2[0], 2) + pow(val1[1] - val2[1], 2)), 4)


def create_new_tile(tiles):
    # First, find the closest tile to the mouse
    mouse_position = pygame.mouse.get_pos()
    closest_tile = None
    shortest_distance = math.inf
    for t in tiles:
        dist = distance_formula(t.center, mouse_position)
        if dist < shortest_distance:
            shortest_distance = dist
            closest_tile = t

    # Then get the created tile's orientation relative to the closest tile
    v0, v1, v2, v3 = closest_tile.vertices
    vertical = 'top'
    horizontal = 'right'
    if distance_formula(v1, mouse_position) >= distance_formula(v3, mouse_position):
        horizontal = 'left'
    if distance_formula(v0, mouse_position) >= distance_formula(v2, mouse_position):
        vertical = 'bottom'
    direction = vertical + '-' + horizontal

    new_kite = Kite()
    new_dart = Dart()

    new_kite.draw(closest_tile, direction)
    new_dart.draw(closest_tile, direction)

    if new_kite in tiles or new_dart in tiles:
        return None

    if kite_is_selected:
        return new_kite
    else:
        return new_dart


def deflate_tiles(tiles_to_deflate):
    new_vertices = []
    new_tiles = []

    for t in tiles_to_deflate:
        if t.name == 'kite':
            for item in t.deflate():
                if item.name == 'dart':
                    update_tiles(item, new_tiles, new_vertices)
                else:
                    update_tiles(item, new_tiles, new_vertices, False)

    return new_tiles, new_vertices


def inflate_tiles(vertices):
    new_vertices = []
    new_tiles = []

    for vert in vertices:
        if vert.name == 'deuce':
            kite_right, kite_left, dart = None, None, None
            for congruence in vert.congruent_vertices:
                if congruence[0].name == 'kite':
                    if kite_right is None:
                        kite_right = congruence[0]
                    else:
                        kite_left = congruence[0]
                else:
                    dart = congruence[0]

            # swap kites if incorrectly assigned
            if compare_coord(kite_right.vertices[1], kite_left.vertices[3]):
                switch = kite_left
                kite_left = kite_right
                kite_right = switch

            # inflated kite vertices
            v0 = kite_left.vertices[1]
            v1 = kite_left.vertices[2]
            v2 = dart.vertices[0]
            v3 = kite_right.vertices[2]
            inflated_kite = Kite()
            inflated_kite.set_vertices([v0, v1, v2, v3])
            update_tiles(inflated_kite, new_tiles, new_vertices, False)

        elif vert.name == 'jack':
            dart_right, dart_left, kite = None, None, None
            for congruence in vert.congruent_vertices:
                if congruence[0].name == 'kite':
                    if congruence[1] == 0:
                        kite = congruence[0]
                else:
                    if congruence[1] == 1:
                        dart_left = congruence[0]
                    else:
                        dart_right = congruence[0]

            # inflated dart vertices
            v0 = kite.vertices[2]
            v1 = dart_left.vertices[0]
            v2 = kite.vertices[0]
            v3 = dart_right.vertices[0]
            inflated_dart = Dart()
            inflated_dart.set_vertices([v0, v1, v2, v3])
            update_tiles(inflated_dart, new_tiles, new_vertices, False)

    return new_tiles, new_vertices


def move_tiles(tiles, displacement):

    new_vertices = []
    new_tiles = []
    for t in tiles:
        displaced_vertices = []
        for vert in t.vertices:
            new_vertex = (vert[0] + displacement[0], vert[1] + displacement[1])
            displaced_vertices.append(new_vertex)
        t.set_vertices(displaced_vertices)
        update_tiles(t, new_tiles, new_vertices)
    return new_vertices


# -------------- Pre-Game Initialization ----------------
#
initial_tile.initial_shape((DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2), unit_length=UNIT_LENGTH)
all_tiles.append(initial_tile)
for vertex_coordinates in initial_tile.vertices:
    all_vertices.append(Vertex(initial_tile, vertex_coordinates))
#
# --------------------- Game Loop -----------------------
while game_is_running:

    # Background color
    DISPLAY.fill((0, 0, 0))

    # Event handler
    for event in pygame.event.get():

        # Exit program
        if event.type == pygame.QUIT:
            game_is_running = False

        # This creates the highlighted tile for user visuals
        if event.type == pygame.MOUSEMOTION:
            guide_tile = []
            created_tile = create_new_tile(all_tiles)
            if guide_tile_active:
                guide_tile.append(created_tile)

        # Places a new tile where the user clicks
        if event.type == pygame.MOUSEBUTTONUP:
            # Left mouse button pressed
            if event.button == 1:
                created_tile = create_new_tile(all_tiles)
                if created_tile is None:
                    print('tile already exists')
                else:
                    start = time.time()

                    all_tiles.append(created_tile)
                    update_vertices(created_tile, all_vertices)
                    force_tiles(all_vertices, all_tiles)

                    end = time.time()
                    print('build time: ', round(end - start, 4), 'sec')
                    tiles_generated = show_stats(tiles_generated)

        # Key press event handlers
        if event.type == pygame.KEYUP:

            # ---------- change tile type ------------
            if event.key == pygame.K_SPACE:
                print('Next shape: dart') if kite_is_selected else print('Next shape: kite')
                kite_is_selected = not kite_is_selected

            # ------------- debug ---------------
            elif event.key == pygame.K_t:
                print('debug')
                force_tiles(all_vertices, all_tiles)

            # ---------- wire frame mode ------------
            elif event.key == pygame.K_c:
                wire_frame_active = not wire_frame_active

            # ---------- exit ------------
            elif event.key == pygame.K_ESCAPE:
                game_is_running = False

            # ------------- assign new colors ---------------
            elif event.key == pygame.K_e:   # random
                for tile in all_tiles:
                    tile.set_random_color()
            elif event.key == pygame.K_q:   # all black
                for tile in all_tiles:
                    tile.color = (0, 0, 0)

            # ------------- reset ---------------
            elif event.key == pygame.K_r:
                initial_tile.initial_shape((DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2), unit_length=UNIT_LENGTH)
                all_tiles = [initial_tile]
                all_vertices = []
                update_vertices(initial_tile, all_vertices)

            # ------------- run build animation ---------------
            elif event.key == pygame.K_b:
                build_animation_active = True

            elif event.key == pygame.K_v:
                build_animation_active_reverse = True

            # ------------- guide tile ---------------
            elif event.key == pygame.K_f:
                guide_tile_active = not guide_tile_active

            # ------------- inflate ---------------
            elif event.key == pygame.K_x:
                print('inflating')
                start = time.time()
                returned_tiles, returned_vertices = inflate_tiles(all_vertices)
                if returned_tiles:
                    all_tiles = returned_tiles
                    all_vertices = returned_vertices
                    force_tiles(all_vertices, all_tiles)
                    tiles_generated = show_stats(tiles_generated)

                else:
                    print('can\'t inflate')
                end = time.time()
                print('build time: ', round(end - start, 4), 'sec')

            # ------------- deflate ---------------
            elif event.key == pygame.K_z:  # deflate
                print('deflating')
                start = time.time()
                all_tiles, all_vertices = deflate_tiles(all_tiles)
                force_tiles(all_vertices, all_tiles)
                tiles_generated = show_stats(tiles_generated)
                end = time.time()
                print('build time: ', round(end - start, 4), 'sec')

            # ------------- move tiles ---------------
            elif event.key == pygame.K_w and len(all_tiles) < 1000:
                all_vertices = move_tiles(all_tiles, (0, -displacement_amount))
                force_tiles(all_vertices, all_tiles)
            elif event.key == pygame.K_s and len(all_tiles) < 1000:
                all_vertices = move_tiles(all_tiles, (0, displacement_amount))
                force_tiles(all_vertices, all_tiles)
            elif event.key == pygame.K_a and len(all_tiles) < 1000:
                all_vertices = move_tiles(all_tiles, (-displacement_amount, 0))
                force_tiles(all_vertices, all_tiles)
            elif event.key == pygame.K_d and len(all_tiles) < 1000:
                all_vertices = move_tiles(all_tiles, (displacement_amount, 0))
                force_tiles(all_vertices, all_tiles)

            # ------------- recolor vertices ---------------
            elif event.key == pygame.K_1:
                for vertex in all_vertices:
                    if vertex.name == 'sun':
                        for val in vertex.congruent_vertices:
                            fail = val[0]
                            fail.set_random_color()
            elif event.key == pygame.K_2:
                for vertex in all_vertices:
                    if vertex.name == 'star':
                        for val in vertex.congruent_vertices:
                            fail = val[0]
                            fail.set_random_color()
            elif event.key == pygame.K_3:
                for vertex in all_vertices:
                    if vertex.name == 'deuce':
                        for val in vertex.congruent_vertices:
                            fail = val[0]
                            fail.set_random_color()
            elif event.key == pygame.K_4:
                for vertex in all_vertices:
                    if vertex.name == 'jack':
                        for val in vertex.congruent_vertices:
                            fail = val[0]
                            fail.set_random_color()
            elif event.key == pygame.K_5:
                for vertex in all_vertices:
                    if vertex.name == 'queen':
                        for val in vertex.congruent_vertices:
                            fail = val[0]
                            fail.set_random_color()
            elif event.key == pygame.K_6:
                for vertex in all_vertices:
                    if vertex.name == 'king':
                        for val in vertex.congruent_vertices:
                            fail = val[0]
                            fail.set_random_color()
            elif event.key == pygame.K_TAB:
                for vertex in all_vertices:
                    if vertex.name == 'edge':
                        for val in vertex.congruent_vertices:
                            fail = val[0]
                            fail.color = (255, 255, 255)

        # Pygame Drawing
        if build_animation_active:
            temps = all_tiles.copy()
            temps.sort()
            # temps.reverse()
            for end in range(1, int((len(temps) + 1)/4)):
                end *= 4
                for index, tile in enumerate(temps[:end]):
                    if wire_frame_active:
                        pygame.draw.polygon(DISPLAY, tile.color, tile.vertices, width=2)
                    else:
                        pygame.draw.polygon(DISPLAY, tile.color, tile.vertices, width=0)
                pygame.display.update()

                build_time = 1
                if build_time == 0:
                    build_time = 1
                pygame.time.wait(build_time)
            build_animation_active = False
        elif build_animation_active_reverse:
            temps = all_tiles.copy()
            temps.sort()
            temps.reverse()
            for end in range(1, int((len(temps) + 1)/4)):
                end *= 4
                for index, tile in enumerate(temps[:end]):
                    if wire_frame_active:
                        pygame.draw.polygon(DISPLAY, tile.color, tile.vertices, width=2)
                    else:
                        pygame.draw.polygon(DISPLAY, tile.color, tile.vertices, width=0)
                pygame.display.update()

                build_time = 1
                if build_time == 0:
                    build_time = 1
                pygame.time.wait(build_time)
            build_animation_active_reverse = False
        else:
            if wire_frame_active:
                for index, tile in enumerate(all_tiles):
                    pygame.draw.polygon(DISPLAY, tile.color, tile.vertices, width=2)
                if guide_tile:
                    if guide_tile[0] is not None:
                        pygame.draw.polygon(DISPLAY, (255, 255, 255), guide_tile[0].vertices, width=0)
            else:
                for index, tile in enumerate(all_tiles):
                    pygame.draw.polygon(DISPLAY, tile.color, tile.vertices, width=0)
                if guide_tile:
                    if guide_tile[0] is not None:
                        pygame.draw.polygon(DISPLAY, (255, 255, 255), guide_tile[0].vertices, width=2)

        pygame.display.update()
