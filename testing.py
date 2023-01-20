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
UNIT_LENGTH = 60

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


def add_tile(neighbor_tile):
    # Determines which tile's edge is closest to the mouse click
    f0, f1, f2, f3 = neighbor_tile.vertex_coordinates
    vertical = 'top' if dist(f0) <= dist(f2) else 'bottom'
    horizontal = 'right' if dist(f1) <= dist(f3) else 'left'
    direction = vertical + '-' + horizontal

    g0, g1, g2, g3 = neighbor_tile.vertices

    if direction == 'top-right' and (g0.name != 'edge' or g1.name != 'edge'):
        return False
    elif direction == 'bottom-right' and (g1.name != 'edge' or g2.name != 'edge'):
        return False
    elif direction == 'bottom-left' and (g2.name != 'edge' or g3.name != 'edge'):
        return False
    elif direction == 'top-left' and (g3.name != 'edge' or g0.name != 'edge'):
        return False
    print(g0.name, g1.name, g2.name, g3.name)
    print(direction)

    new_tile = Kite()
    new_tile.draw(neighbor_tile, direction)

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

    linked_vertices, return_vertices = form_vertices(new_tile, [v0, v1, v2, v3])
    new_tile.vertices = linked_vertices

    return new_tile, return_vertices


def form_vertices(tile, vertices):
    v0, v1, v2, v3 = vertices
    return_vertices = []
    if bool(v0) + bool(v1) + bool(v2) + bool(v3) == 2:  # Need to figure out the single False condition
        if (not v0 and not v1) or (not v2 and not v3):
            switch = True if not v0 or not v1 else False
            if not v0:
                v0 = Vertex(tile.vertex_coordinates[0], [v3])
                return_vertices.append(v0)
                v3.adjacent_vertices.append(v0)

            if not v1:
                v1 = Vertex(tile.vertex_coordinates[1], [v2])
                return_vertices.append(v1)
                v2.adjacent_vertices.append(v1)

            if not v2:
                v2 = Vertex(tile.vertex_coordinates[2], [v1])
                return_vertices.append(v2)
                v1.adjacent_vertices.append(v2)

            if not v3:
                v3 = Vertex(tile.vertex_coordinates[3], [v0])
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
                v0 = Vertex(tile.vertex_coordinates[0], [v1])
                return_vertices.append(v0)
                v1.adjacent_vertices.append(v0)

            if not v1:
                v1 = Vertex(tile.vertex_coordinates[1], [v0])
                return_vertices.append(v1)
                v0.adjacent_vertices.append(v1)

            if not v2:
                v2 = Vertex(tile.vertex_coordinates[2], [v3])
                return_vertices.append(v2)
                v3.adjacent_vertices.append(v2)

            if not v3:
                v3 = Vertex(tile.vertex_coordinates[3], [v2])
                return_vertices.append(v3)
                v2.adjacent_vertices.append(v3)

            if switch:
                v1.adjacent_vertices.append(v2)
                v2.adjacent_vertices.append(v1)
            else:
                v0.adjacent_vertices.append(v3)
                v3.adjacent_vertices.append(v0)

    elif bool(v0) + bool(v1) + bool(v2) + bool(v3) == 1:
        print('Coming soon')
    else:
        print('3 False?')

    v0.vertex_components.append((tile, 0))
    v1.vertex_components.append((tile, 1))
    v2.vertex_components.append((tile, 2))
    v3.vertex_components.append((tile, 3))

    return [v0, v1, v2, v3], return_vertices


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
            # Left mouse button pressed
            if event.button == 1:
                x, y = pygame.mouse.get_pos()
                closest_tile = all_tiles[
                    min(range(len(all_tiles)), key=lambda i: math.sqrt((all_tiles[i].center[0] - x) ** 2 +
                                                                       (all_tiles[i].center[1] - y) ** 2))]
                tile_created = add_tile(closest_tile)

                if tile_created:
                    all_tiles.append(tile_created[0])
                    all_vertices.extend(tile_created[1])
                    force_tiles(all_tiles, all_vertices)
                    tile_count = len(all_tiles)

                    total = 0
                    for vertex in all_vertices:
                        for adj in vertex.adjacent_vertices:
                            total += 1
                    print('tiles: {} vertices: {} adjacent: {}'.format(len(all_tiles), len(all_vertices), total))
                else:
                    print('Cannot place tile.')

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

        # Display tiles with pygame
        for index, t in enumerate(all_tiles[0:tile_count]):
            pygame.draw.polygon(DISPLAY, t.color, t.vertex_coordinates, width=0)

        size = 4
        for vt in all_vertices:
            if vt.name == 'edge':
                pygame.draw.circle(DISPLAY, (255, 255, 0), vt.coordinates, size)
            elif vt.name == 'ace':
                pygame.draw.circle(DISPLAY, (0, 0, 234), vt.coordinates, size)
            elif vt.name == 'deuce':
                pygame.draw.circle(DISPLAY, (150, 0, 255), vt.coordinates, size)
            elif vt.name == 'star':
                pygame.draw.circle(DISPLAY, (0, 255, 35), vt.coordinates, size)
            elif vt.name == 'sun':
                pygame.draw.circle(DISPLAY, (255, 5, 255), vt.coordinates, size)

        pygame.display.update()
