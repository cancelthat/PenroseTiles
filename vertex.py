class Vertex:
    # change coordinates to a 2d list, rather a tuple
    def __init__(self, coordinates, name='edge'):
        self.coordinates = coordinates
        self.name = name
        self.congruent_vertices = []  # ex: [(Dart(), 0), (Dart(), 0), (Kite(), 3)]

    def __eq__(self, other):
        value = (self.coordinates[0] - other.coordinates[0]) + (self.coordinates[1] - other.coordinates[1])
        if abs(value) < 0.001:
            return True
        return False
