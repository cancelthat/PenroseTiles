class Vertex:

    def __init__(self, coordinates, adjacent_vertices=None):
        self.coordinates = coordinates
        self.name = 'edge'
        self.adjacent_vertices = [] if adjacent_vertices is None else adjacent_vertices
        self.vertex_components = []  # ex: [(Dart(), 0), (Dart(), 0), (Kite(), 3)]
