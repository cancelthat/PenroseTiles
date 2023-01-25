import copy

import pygame
import math
import time

from tilesTest import Tile
from kite import Kite
from dart import Dart
from vertexTest import Vertex
from alTest import force_tiles, vertex_exists, add_kite, add_dart

# Initializer
pygame.init()

# Display Dimensions
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 750
DISPLAY = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

# Boolean switch to close the program
game_is_running = True

# Tile size
UNIT_LENGTH = 18

# Create the first tile
initial_tile = Kite()
initial_tile.initial_shape((DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2), unit_length=UNIT_LENGTH)

# List of all Tiles
all_tiles = [initial_tile]
tile_count = len(all_tiles)
# List of all Vertices
all_vertices = []

for v in initial_tile.vertex_coordinates:
    all_vertices.append(Vertex(v))
all_vertices[0].adjacent_vertices = [all_vertices[1], all_vertices[3]]
all_vertices[2].adjacent_vertices = [all_vertices[1], all_vertices[3]]
all_vertices[1].adjacent_vertices = [all_vertices[0], all_vertices[2]]
all_vertices[3].adjacent_vertices = [all_vertices[0], all_vertices[2]]

all_vertices[0].vertex_components.append((initial_tile, 0))
all_vertices[1].vertex_components.append((initial_tile, 1))
all_vertices[2].vertex_components.append((initial_tile, 2))
all_vertices[3].vertex_components.append((initial_tile, 3))
initial_tile.vertices = copy.copy(all_vertices)


# Distance from a point to the cursor
def dist(p):
    return math.sqrt((p[0] - pygame.mouse.get_pos()[0]) ** 2 + (p[1] - pygame.mouse.get_pos()[1]) ** 2)


def has_neighbor(neighbor_tile, direction):
    g0, g1, g2, g3 = neighbor_tile.vertices

    if direction == 'top-right' and (g0.name != 'edge' or g1.name != 'edge'):
        return True
    elif direction == 'bottom-right' and (g1.name != 'edge' or g2.name != 'edge'):
        return True
    elif direction == 'bottom-left' and (g2.name != 'edge' or g3.name != 'edge'):
        return True
    elif direction == 'top-left' and (g3.name != 'edge' or g0.name != 'edge'):
        return True
    return False


# --------------------------------------------------- Main Function ---------------------------------------------------
while game_is_running:

    # Background color
    DISPLAY.fill((0, 0, 0))

    # Event handler
    for event in pygame.event.get():

        # Exit program
        if event.type == pygame.QUIT:
            game_is_running = False

        # Places a new tile where the user clicks
        if event.type == pygame.MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            closest_tile = all_tiles[
                min(range(len(all_tiles)), key=lambda i: math.sqrt((all_tiles[i].center[0] - x) ** 2 +
                                                                   (all_tiles[i].center[1] - y) ** 2))]
            f0, f1, f2, f3 = closest_tile.vertex_coordinates
            vertical = 'top' if dist(f0) <= dist(f2) else 'bottom'
            horizontal = 'right' if dist(f1) <= dist(f3) else 'left'
            tile_direction = vertical + '-' + horizontal

            if has_neighbor(closest_tile, tile_direction):
                print('Cannot place tile')
                print(tile_direction)
                continue
            else:
                if event.button == 1:  # Left mouse button pressed
                    add_kite(closest_tile, tile_direction, all_tiles, all_vertices)

                elif event.button == 3:  # Right mouse button pressed
                    add_dart(closest_tile, tile_direction, all_tiles, all_vertices)

                force_tiles(all_tiles, all_vertices)
                tile_count = len(all_tiles)

                # print info
                total = 0
                for vertex in all_vertices:
                    for adj in vertex.adjacent_vertices:
                        total += 1
                print('tiles: {} vertices: {} adjacent: {}'.format(len(all_tiles), len(all_vertices), total))

        # Key press event handlers
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                game_is_running = False
            elif event.key == pygame.K_w:
                if tile_count < len(all_tiles):
                    tile_count += 1
            elif event.key == pygame.K_s:
                if tile_count > 0:
                    tile_count -= 1
            elif event.key == pygame.K_e:
                if tile_count < len(all_tiles)-100:
                    tile_count += 100
                else:
                    tile_count = len(all_tiles)
            elif event.key == pygame.K_d:
                if tile_count > 100:
                    tile_count -= 100
                else:
                    tile_count = 0
            elif event.key == pygame.K_e:
                vertex_count = [0, 0, 0, 0, 0, 0, 0, 0]
                for vt in all_vertices:
                    if vt.name == 'edge':
                        vertex_count[0] += 1
                    elif vt.name == 'ace':
                        vertex_count[1] += 1
                    elif vt.name == 'deuce':
                        vertex_count[2] += 1
                    elif vt.name == 'star':
                        vertex_count[3] += 1
                    elif vt.name == 'sun':
                        vertex_count[4] += 1
                    elif vt.name == 'jack':
                        vertex_count[5] += 1
                    elif vt.name == 'queen':
                        vertex_count[6] += 1
                    elif vt.name == 'king':
                        vertex_count[7] += 1
                print('edge: {}  ace: {}  deuce: {}  star: {}  sun: {}  jack: {}  queen: {}  king: {}'.format(
                    vertex_count[0], vertex_count[1], vertex_count[2], vertex_count[3], vertex_count[4],
                    vertex_count[5], vertex_count[6], vertex_count[7]))
                print('adjacent total = ', (vertex_count[1] * 3) + (vertex_count[2] * 4) + (5 * (
                        vertex_count[3] + vertex_count[4] + vertex_count[5] + vertex_count[6] + vertex_count[7])),
                      '+ edge vertex count')

        # Display tiles with pygame
        for index, t in enumerate(all_tiles[0:tile_count]):
            pygame.draw.polygon(DISPLAY, t.color, t.vertex_coordinates, width=0)

        size = 1
        for vt in all_vertices:
            if vt.name == 'edge':
                pygame.draw.circle(DISPLAY, (255, 255, 0), vt.coordinates, 4)
            elif vt.name == 'ace':
                pygame.draw.circle(DISPLAY, (0, 0, 234), vt.coordinates, size)
            elif vt.name == 'deuce':
                pygame.draw.circle(DISPLAY, (150, 0, 255), vt.coordinates, size)
            elif vt.name == 'star':
                pygame.draw.circle(DISPLAY, (0, 255, 35), vt.coordinates, size)
            elif vt.name == 'sun':
                pygame.draw.circle(DISPLAY, (255, 5, 255), vt.coordinates, size)
            elif vt.name == 'jack':
                pygame.draw.circle(DISPLAY, (200, 5, 0), vt.coordinates, size)
            elif vt.name == 'queen':
                pygame.draw.circle(DISPLAY, (255, 225, 255), vt.coordinates, size)
            elif vt.name == 'king':
                pygame.draw.circle(DISPLAY, (255, 127, 0), vt.coordinates, size)

        pygame.display.update()
