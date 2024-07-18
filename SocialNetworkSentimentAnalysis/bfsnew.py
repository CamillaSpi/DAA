def BFSclassic(g, s, discovered):
    """Perform BFS of the undiscovered portion of Graph g starting at Vertex s.
    discovered is a dictionary mapping each vertex to the edge that was used to
    discover it during the BFS.
    Newly discovered vertices will be added to the dictionary as a result."""

    level = [s]  # first level includes only s
    while len(level) > 0:
        next_level = []  # prepare to gather newly found vertices
        for u in level:
            for e in g.incident_edges(u):  # for every outgoing edge from u
                if e.element() is not None and e.element() > 0:  # if the element of the edge is not positive it means that no more flow can be sent on that edge
                    v = e.opposite(u)
                    if v not in discovered:  # v is an unvisited vertex
                        discovered[v] = e  # e is the edge that discovered v
                        next_level.append(v)  # v will be further considered in next pass
        level = next_level  # relabel 'next' level to become current


def BFSoptimized(g, sorg, dest, discovered):
    """This is a different version of BFS, used in order to found a path
    from the source sorg and the destination dest passed as parameter.
    discovered is a dictionary mapping each vertex to the edge that was used to
    discover it during the BFS. As soon as a path from the source to the destination
    is found, the search is stopped with element in discovered inserted until that moment"""
    level = [sorg]  # first level includes only s
    while len(level) > 0:
        next_level = []  # prepare to gather newly found vertices
        for u in level:
            for e in g.incident_edges(u):  # for every outgoing edge from u
                if e.element() > 0:
                    v = e.opposite(u)
                    if v not in discovered:  # v is an unvisited vertex
                        final_edge = g.get_edge(v, dest)  # search if there is an edge from the current vertex to the destination
                        discovered[v] = e
                        if final_edge is not None and final_edge.element() > 0:  # if there is an edge from the current node to the destination with positive value the path has been found and so the search can be stopped
                            discovered[dest] = final_edge
                            return
                        next_level.append(v)  # v will be further considered in next pass
        level = next_level  # relabel 'next' level to become current


def edges_path(u, v, discovered):
    """Return a list of edges comprising the directed path from u to v,
    or an empty list if v is not reachable from u.
    discovered is a dictionary resulting from a previous call to BFSoptimized started at u.
    It also calculates the bottleneck of the path so the edge on which less flow can be sent, and return it. """
    path = []  # empty path by default
    min = None
    if v in discovered:
        walk = v
        while walk is not u:
            e = discovered[walk]  # find edge leading to walk
            walk = e.opposite(walk)
            path.append(e)
            if min is None or e.element() < min:  # calculate the bottleneck of the path
                min = e.element()
    return path, min
