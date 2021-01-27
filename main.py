import pygame
import math
import time
from tiles import Tile
from forced_tiles_recursion_functions import force_tiles, update_dictionary, remove_completed_vertices
from deflation import deflate

# Global Constants
PHI = (1 + math.sqrt(5)) / 2  # 1.618033988749895
STD_LEN = 12

# Initializer
pygame.init()

# Display
screenX = 800
screenY = 750
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
dark_mode = False
build_animation = False

# Pregame Initializations
initial_tile = Tile(name='kite', tile_id=0)
initial_tile.initial_shape(((screenX / 2) - 0, round(screenY / 2 - STD_LEN * PHI, 4) + 0), length=STD_LEN)

# Information Holders
all_tiles = [initial_tile]
vertex_dictionary = {}  # { vertex: (Tile, vertex_index) }
tiles_generated = 1


def show_stats(amount):
    print('edge vertices: ', len(vertex_dictionary))
    print('tiles generated: ', len(all_tiles)-amount)
    print('total tiles: ', len(all_tiles))
    print('------------------------------------------')
    return len(all_tiles)


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


#
# -------------- Pre-Game Initialization ----------------
#
update_dictionary(vertex_dictionary, initial_tile)
#
# -------------- Game Loop ----------------
#
while game_is_running:

    # Background color
    screen.fill((0, 0, 0))
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
                start = time.time()
                # Append new tile
                all_tiles.append(created_tile)
                # Update vertex dictionary
                update_dictionary(vertex_dictionary, created_tile)
                # Check for forced tiles
                force_tiles(vertex_dictionary, all_tiles)
                end = time.time()
                print('build time: ', round(end-start, 4), 'sec')
                tiles_generated = show_stats(tiles_generated)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                print('Next shape: dart') if kite_is_selected else print('Next shape: kite')
                kite_is_selected = not kite_is_selected
            elif event.key == pygame.K_k:   # wire-frame
                dark_mode = not dark_mode
            elif event.key == pygame.K_l:   # new random colors
                for t in all_tiles:
                    t.set_random_color()
            elif event.key == pygame.K_r:   # reset
                all_tiles = [initial_tile]
                vertex_dictionary = {}
                update_dictionary(vertex_dictionary, initial_tile)
            elif event.key == pygame.K_b:   # build animation
                build_animation = True
            elif event.key == pygame.K_c:   # color current tiles
                for tile in all_tiles:
                    tile.color = (5, 13, 174)
            elif event.key == pygame.K_d:   # deflate
                start = time.time()
                all_tiles, vertex_dictionary = deflate(all_tiles)
                force_tiles(vertex_dictionary, all_tiles)
                tiles_generated = show_stats(tiles_generated)
                end = time.time()
                print('build time: ', round(end - start, 4), 'sec')
        if build_animation:
            for bacon in range(1, len(all_tiles)+1):
                for eggs in all_tiles[:bacon]:
                    if dark_mode:
                        pygame.draw.polygon(screen, eggs.color, eggs.vertices, width=0)
                    else:
                        pygame.draw.polygon(screen, eggs.color, eggs.vertices, width=2)
                pygame.display.update()

                build_time = int((3.25*1000)/len(all_tiles))
                if build_time == 0:
                    build_time = 1
                pygame.time.wait(build_time)
            build_animation = False
        elif dark_mode:
            for eggs in all_tiles:
                pygame.draw.polygon(screen, eggs.color, eggs.vertices, width=0)
        else:
            for eggs in all_tiles:
                pygame.draw.polygon(screen, eggs.color, eggs.vertices, width=2)

        pygame.display.update()
