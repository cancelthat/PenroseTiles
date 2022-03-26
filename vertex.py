class Vertex:
    # change coordinates to a 2d list, rather a tuple
    def __init__(self, tile_to_add, coordinates, name='edge'):
        self.coordinates = coordinates
        self.name = name
        # list of 2D tuples, holding a tile and the tile's congruent vertex. ex [(Kite(), 1), (Dart(), 0)]
        self.congruent_vertices = []
        for i, v0 in enumerate(tile_to_add.vertices):
            if v0 == coordinates:
                self.congruent_vertices.append((tile_to_add, i))

    def __eq__(self, other):
        value = (self.coordinates[0] - other.coordinates[0]) + (self.coordinates[1] - other.coordinates[1])
        if abs(value) < 0.001:
            return True
        return False
