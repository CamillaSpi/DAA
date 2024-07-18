from graph import Graph


class ExtendedGraph(Graph) :
    """Representation of an extension of a simple graph using an adjacency map."""

    class ExtendedEdge(Graph.Edge):
        """Structure for an edge of the extended graph
        having more features than the edge of the class Graph ."""


        def changeElement(self, newElement):
            """Function to change the element associated to the extendedEdge.
            It takes in imput the new value of the edge and if it is not None
            changes the value of the element, otherwise the value remains
            the previous one"""
            if newElement is not None:
               self._element = newElement

    def insert_edge(self, u, v,  x=None):
        """Insert and return a new ExtendedEdge from u to v with associated element x.
        Raise a ValueError if u and v are not vertices of the graph.
        Raise a ValueError if u and v are already adjacent.
        """
        if self.get_edge(u, v) is not None:      # includes error checking
          raise ValueError('u and v are already adjacent')
        e = self.ExtendedEdge(u, v, x)
        self._outgoing[u][v] = e
        self._incoming[v][u] = e
