import copy

import pygame
import math
import time

from tilesTest import Tile
from kite import Kite
from dart import Dart
from vertexTest import Vertex
from alTest import force_tiles, vertex_exists

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

# List of all Vertices
vertices = []

for v in initial_tile.vertex_coordinates:
    vertices.append(Vertex(v))
vertices[0].adjacent_vertices = [vertices[1], vertices[3]]
vertices[2].adjacent_vertices = [vertices[1], vertices[3]]
vertices[1].adjacent_vertices = [vertices[0], vertices[2]]
vertices[3].adjacent_vertices = [vertices[0], vertices[2]]

vertices[0].vertex_components.append((initial_tile, 0))
vertices[1].vertex_components.append((initial_tile, 1))
vertices[2].vertex_components.append((initial_tile, 2))
vertices[3].vertex_components.append((initial_tile, 3))
initial_tile.vertices = copy.copy(vertices)


def link_vertices(new_vertices, new_tile):
    v0, v1, v2, v3 = new_vertices

    switch = True if not v1 or not v2 else False

    if not v1:
        v1 = Vertex(new_tile.vertex_coordinates[1], [v0])
        vertices.append(v1)
        v0.adjacent_vertices.append(v1)

    if not v2:
        v2 = Vertex(new_tile.vertex_coordinates[2], [v3])
        vertices.append(v2)
        v3.adjacent_vertices.append(v2)

    if switch:
        v1.adjacent_vertices.append(v2)
        v2.adjacent_vertices.append(v1)

    v0.vertex_components.append((new_tile, 0))
    v1.vertex_components.append((new_tile, 1))
    v2.vertex_components.append((new_tile, 2))
    v3.vertex_components.append((new_tile, 3))


# Distance from a point to the cursor
def dist(p):
    x, y = pygame.mouse.get_pos()
    return math.sqrt((p[0] - x) ** 2 + (p[1] - y) ** 2)


def add_tile(tiles):
    # Find the closest tile to the cursor
    x, y = pygame.mouse.get_pos()
    closest_tile = tiles[min(range(len(tiles)), key=lambda i: math.sqrt((tiles[i].center[0] - x) ** 2 +
                                                                        (tiles[i].center[1] - y) ** 2))]
    # Determines which tile's edge is closest to the mouse click
    a0, a1, a2, a3 = closest_tile.vertex_coordinates
    vertical = 'top' if dist(a0) <= dist(a2) else 'bottom'
    horizontal = 'right' if dist(a1) <= dist(a3) else 'left'
    direction = vertical + '-' + horizontal

    v0, v1, v2, v3 = closest_tile.vertices
    if direction == 'top-right':
        if v0.name == 'edge' and v1.name == 'edge':
            new_tile = Kite()
            new_tile.draw(closest_tile, direction)
            all_tiles.append(new_tile)

            # New Vertex object
            d0 = v0
            d1 = vertex_exists(new_tile.vertex_coordinates[1], v0)
            d2 = vertex_exists(new_tile.vertex_coordinates[2], v1)
            d3 = v1

            new_vertices = [d0, d1, d2, d3]
            link_vertices(new_vertices, new_tile)

            switch = True if not d1 or not d2 else False

            if not d1:
                d1 = Vertex(new_tile.vertex_coordinates[1], [d0])
                vertices.append(d1)
                d0.adjacent_vertices.append(d1)

            if not d2:
                d2 = Vertex(new_tile.vertex_coordinates[2], [d3])
                vertices.append(d2)
                d3.adjacent_vertices.append(d2)

            if switch:
                d1.adjacent_vertices.append(d2)
                d2.adjacent_vertices.append(d1)

            d0.vertex_components.append((new_tile, 0))
            d1.vertex_components.append((new_tile, 1))
            d2.vertex_components.append((new_tile, 2))
            d3.vertex_components.append((new_tile, 3))

            new_tile.vertices = [d0, d1, d2, d3]
            return "{} appended.".format(new_tile.name)
    elif direction == 'bottom-right':
        if v1.name == 'edge' and v2.name == 'edge':
            new_tile = Kite()
            new_tile.draw(closest_tile, direction)
            all_tiles.append(new_tile)

            p0 = vertex_exists(new_tile.vertex_coordinates[0], v1)
            p1 = vertex_exists(new_tile.vertex_coordinates[1], v2)
            p2 = v2
            p3 = v1

            switch = True if not p0 or not p1 else False

            if not p0:
                p0 = Vertex(new_tile.vertex_coordinates[0], [p3])
                vertices.append(p0)
                p3.adjacent_vertices.append(p0)

            if not p1:
                p1 = Vertex(new_tile.vertex_coordinates[1], [p2])
                vertices.append(p1)
                p2.adjacent_vertices.append(p1)

            if switch:
                p0.adjacent_vertices.append(p1)
                p1.adjacent_vertices.append(p0)

            p0.vertex_components.append((new_tile, 0))
            p1.vertex_components.append((new_tile, 1))
            p2.vertex_components.append((new_tile, 2))
            p3.vertex_components.append((new_tile, 3))

            new_tile.vertices = [p0, p1, p2, p3]
            return "{} appended.".format(new_tile.name)
    elif direction == 'bottom-left':
        if v2.name == 'edge' and v3.name == 'edge':
            new_tile = Kite()
            new_tile.draw(closest_tile, direction)
            all_tiles.append(new_tile)

            p0 = vertex_exists(new_tile.vertex_coordinates[0], v3)
            p1 = v3
            p2 = v2
            p3 = vertex_exists(new_tile.vertex_coordinates[3], v2)

            switch = True if not p0 or not p3 else False

            if not p0:
                p0 = Vertex(new_tile.vertex_coordinates[0], [p1])
                vertices.append(p0)
                p1.adjacent_vertices.append(p0)

            if not p3:
                p3 = Vertex(new_tile.vertex_coordinates[3], [p2])
                vertices.append(p3)
                p2.adjacent_vertices.append(p3)

            if switch:
                p0.adjacent_vertices.append(p3)
                p3.adjacent_vertices.append(p0)

            p0.vertex_components.append((new_tile, 0))
            p1.vertex_components.append((new_tile, 1))
            p2.vertex_components.append((new_tile, 2))
            p3.vertex_components.append((new_tile, 3))

            new_tile.vertices = [p0, p1, p2, p3]
            return "{} appended.".format(new_tile.name)
    elif direction == 'top-left':
        if v3.name == 'edge' and v0.name == 'edge':
            new_tile = Kite()
            new_tile.draw(closest_tile, direction)
            all_tiles.append(new_tile)

            # New Vertex object
            k0 = v0
            k1 = v3
            k2 = vertex_exists(new_tile.vertex_coordinates[2], v3)
            k3 = vertex_exists(new_tile.vertex_coordinates[3], v0)

            switch = True if not k2 or not k3 else False

            if not k2:
                k2 = Vertex(new_tile.vertex_coordinates[2], [k1])
                vertices.append(k2)
                k1.adjacent_vertices.append(k2)

            if not k3:
                k3 = Vertex(new_tile.vertex_coordinates[3], [k0])
                vertices.append(k3)
                k0.adjacent_vertices.append(k3)

            if switch:
                k2.adjacent_vertices.append(k3)
                k3.adjacent_vertices.append(k2)

            k0.vertex_components.append((new_tile, 0))
            k1.vertex_components.append((new_tile, 1))
            k2.vertex_components.append((new_tile, 2))
            k3.vertex_components.append((new_tile, 3))

            new_tile.vertices = [k0, k1, k2, k3]
            return "{} appended.".format(new_tile.name)
    else:
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
            # Left mouse button pressed
            if event.button == 1:
                tileWasAdded = add_tile(all_tiles)

                if tileWasAdded:
                    print(tileWasAdded)
                    force_tiles(all_tiles, vertices)
                else:
                    print('Can not place tile.')

        # Key press event handlers
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                game_is_running = False

        # Display tiles with pygame
        for index, tile in enumerate(all_tiles):
            pygame.draw.polygon(DISPLAY, tile.color, tile.vertex_coordinates, width=0)

        size = 4
        for vt in vertices:
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
