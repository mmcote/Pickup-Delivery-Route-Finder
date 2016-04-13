import math

class Graph:
    '''A graph has a set of vertices and a set of edges, with each
    edge being an ordered pair of vertices. '''

    def __init__ (self):
        self._alist = {}

    def add_vertex (self, vertex):
        ''' Adds 'vertex' to the graph
        Preconditions: None
        Postconditions: self.is_vertex(vertex) -> True
        '''
        if vertex not in self._alist:
            self._alist[vertex] = set()

    def add_edge (self, source, destination):
        ''' Adds the edge (source, destination)
        Preconditions: None
        Postconditions:
        self.is_vertex(source) -> True,
        self.is_vertex(destination),
        self.is_edge(source, destination) -> True
        '''
        self.add_vertex(source)
        self.add_vertex(destination)
        self._alist[source].add(destination)

    def is_edge (self, source, destination):
        '''Checks whether (source, destination) is an edge
        '''
        return (self.is_vertex(source)
                and destination in self._alist[source])

    def is_vertex (self, vertex):
        '''Checks whether vertex is in the graph.
        '''
        return vertex in self._alist

    def neighbours (self, vertex):
        '''Returns the set of neighbours of vertex. DO NOT MUTATE
        THIS SET.
        Precondition: self.is_vertex(vertex) -> True
        '''
        return self._alist[vertex]

    def vertices (self):
        '''Returns a set-like container of the vertices of this
        graph.'''
        return self._alist.keys()


class UndirectedGraph (Graph):
    '''An undirected graph has edges that are unordered pairs of
    vertices; in other words, an edge from A to B is the same as one
    from B to A.'''

    def add_edge (self, a, b):
        '''We implement this as a directed graph where every edge has its
        opposite also added to the graph'''
        super().add_edge (a, b)
        super().add_edge (b, a)


class WeightedGraph (Graph):
    '''A weighted graph stores some extra information (usually a
    "weight") for each edge.'''

    def add_vertex (self, vertex):
        ''' Adds 'vertex' to the graph
        Preconditions: None
        Postconditions: self.is_vertex(vertex) -> True
        '''
        if vertex not in self._alist:
            self._alist[vertex] = {}

    def add_edge (self, source, destination, weight = None):
        ''' Adds the edge (source, destination) with given weight
        Preconditions: None
        Postconditions:
        self.is_vertex(source) -> True,
        self.is_vertex(destination),
        self.is_edge(source, destination) -> True
        '''
        self.add_vertex(source)
        self.add_vertex(destination)
        self._alist[source][destination] = weight

    def get_weight (self, source, destination):
        '''Returns the weight associated with this edge.
        Precondition: self.is_edge(source, destination) -> True'''
        if self.is_edge(source,destination) != True:
            return float("inf")
        else:
            return self._alist[source][destination]

    def neighbours (self, vertex):
        '''Returns the set of neighbours of vertex.
        Precondition: self.is_vertex(vertex) -> True
        '''
        return self._alist[vertex].keys()

    def neighbours_and_weights (self, vertex):
        return self._alist[vertex].items()
