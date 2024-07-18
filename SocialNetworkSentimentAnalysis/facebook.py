from bfsnew import BFSoptimized, edges_path, BFSclassic
from extendedGraph import ExtendedGraph
from graph import Graph


def create_undirected_graph(V, E):
    """This function is used from the facebook_enmy function in order to create an undirected graph.
    The function takes in input a set V containing the voters,
    and a dictionary E containing the correspondence between pairs of voters that have a friendship relationship on facebook
    and their enmity level.
    The graph created is undirected and for each edge the corresponding element refers to the enmity level of the pair.
    After the creation of the graph a dictionary is created containing the correspondence between the vertex and its weights
    that is the difference between the sum of values on edges whose opposite is in the same set and the sum of values
    on edges whose opposite is not in the same set.
    It returns the graph created and the dictionary with vertex and their weights."""
    vertices = {}  # a dictionary containing as keys the element representing the voters and as values the vertex associated
    weighted_vertex = {}  # a dictionary containing as keys the vertices and as values the weight associated to the vertex
    graph = Graph()
    for vertex_content in V:
        vertex = graph.insert_vertex(vertex_content)  # insert vertex in the graph, containing as element the voter
        vertices[
            vertex_content] = vertex  # create a relation between element contained into vertex and the vertex itself
    for edge in E:
        graph.insert_edge(vertices[edge[0]], vertices[edge[1]], E[edge])  # insert edge in the graph containing as element the enmity level of the pair
    for vertex in vertices:  # for each vertex establish its initial weight
        weight = 0
        for incident_edge in graph.incident_edges(vertices[vertex]):  # at the creation moment, all the vertices are imaginatively in the same set
            weight += incident_edge.element()  # so all the value of incident edges are added
        weighted_vertex[vertices[vertex]] = weight
    return graph, weighted_vertex


def facebook_enmy(V, E):
    """This function takes in input a set V containing the voters,
    and a dictionary E containing the correspondence between pairs of voters that have a friendship relationship on facebook and their enmity level.
    The function decrees the division of voters in Democrats and Republicans so that the level of enmity among the two groups is as
    large as possible. Hence, the level of enmity in a set of voters is computed as the sum of enmities among each pair of these voters
    that are friends on the social network.
    After creating an undirected graph in an appropriate way to solve the problem, the idea is to sort vertices according to their
    weights, to choose the major and establish in which set it is convenient to insert it in order to maximize the enmity
    between the two groups.
    The purpose of the function is try to get out of the local maximums to reach the absolute maximums, collecting a series
    of solutions, sometimes even worse ones, to then choose the best one at the end.
    It returns the set of voters who vote for Democrats and those who vote for Republicans."""
    democratic = []  # voters who vote for Democrats
    republican = []  # voters who vote for Republicans
    moved = {}  # a dictionary having as keys the index of solution and as value the best element to move for that solution
    solution = {}  # a dictionary having as keys the index of solution and as value the cut between sets calculated in that solution

    graph, weighted_vertex = create_undirected_graph(V, E)  # builds the graph and assign to each vertex its weight
    solution_cut = 0  # at beginning the cut between the two sets is equal to zero because all vertex are supposed to stay in the same set
    for i in range(len(graph.vertices())):  # the number of solutions collected is equal to the number of voters
        weighted_ordered_Vertex = sorted(weighted_vertex.items(), key=lambda x: x[1], reverse=True)  # the voters are ordered in descending order
        vertex_to_move = weighted_ordered_Vertex[0]  # each time the vertex to move is the greater because it is the locally best solution
        solution_cut = solution_cut + vertex_to_move[1]  # the cut associated with the solution is increased of the weight of the moved vertex
        moved[i] = vertex_to_move[0]  # the moved vertex is saved associated to current index solution
        weighted_vertex.pop(vertex_to_move[0])  # the moved vertex is removed from the set of vertices not yet moved
        for incident_edge in graph.incident_edges(vertex_to_move[0]):  # for each vertex connected to the moved vertex it is necessary to change its weight
            other_node = incident_edge.opposite(vertex_to_move[0])
            if other_node in weighted_vertex:  # it is necessary to change the weight only if the opposite vertex has not yet been moved
                weighted_vertex[other_node] = weighted_vertex[other_node] - 2 * incident_edge.element()  # the weight of the vertex is modified subtracting from the previous weight two times the value of the edge connecting the pair
        solution[i] = solution_cut  # the cut associated with the index solution is set to the current solution cut

    max = 0
    index = 0
    for sol in solution:  # among the collecting solutions is searched that with the maximum cut associated
        if solution[sol] >= max:
            max = solution[sol]  # the maximum cut found is saved
            index = sol  # the solution index associated with the best solution is saved
    for k in range(len(moved)):
        if k <= index:  # element moved before the best solution contributes to it, and so they must be moved
            republican.append(moved[k].element())  # these elements are added to republican set
        else:
            democratic.append(moved[k].element())  # the elements moved after the best solution found, do not contribute to it, and so they must not be moved, so they are added to democratic set
    return democratic, republican


def create_directed_graph(V, E):
    """This function is used from the facebook_friend function in order to create a network flow.
    The function takes in input a dictionary V containing the correspondence between voters and the likelihood for each of them for Democrats and for Republicans,
    and a dictionary E containing the correspondence between pairs of voters that have a friendship relationship on facebook and their friendship level.
    To create the network flow, two more vertices are inserted, the superSorg and the superTarg, in addiction to the set of voters passed.
    The edge inserted are of three types:
    those from the superSorg to all the other nodes, having as element the likelihood for that voter to vote for Democrats
    those from all the vertices to the superTarget, having as element the likelihood for that voter to vote for Republicans
    those between vertices, in both directions, having as elements the friendship value between voters"""

    vertices = {}
    netFlow = ExtendedGraph(True)  # an extended graph directed
    superSorg = netFlow.insert_vertex("SuperSorg")  # additional node representing the source
    superTarg = netFlow.insert_vertex("SuperTarget")  # additional node representing the destination
    for voter in V:
        voterVertex = netFlow.insert_vertex(voter)  # new vertex containing as element the corresponding voter
        vertices[voter] = voterVertex
        netFlow.insert_edge(superSorg, voterVertex, V[voter][0])  # edge from source to the inserted vertex
        netFlow.insert_edge(voterVertex, superTarg, V[voter][1])  # edge from the inserted vertex to destination
    for friendship in E:
        netFlow.insert_edge(vertices[friendship[0]], vertices[friendship[1]], E[friendship])  # edge between the pair of voter in the forward direction
        netFlow.insert_edge(vertices[friendship[1]], vertices[friendship[0]], E[friendship])  # edge between the pair of voter in the reverse direction
    return netFlow, vertices, superSorg, superTarg


def define_path(netFlow, superSorg, superTarg):
    """This function define a path from the source to the destination in the graph passed as parameters.
    It is used a function BFSoptimized so that in discovered are inserted all the vertices visited from the source to the destination,
    associated with the edge used to discovered them. Then the path, so traveled edges, are returned from the edges_path function, also with
    the bottleneck of the path."""
    discovered = {}
    BFSoptimized(netFlow, superSorg, superTarg, discovered)
    path, bottleneck = edges_path(superSorg, superTarg, discovered)
    return path, bottleneck


def facebook_friend(V, E):
    """This function establishes the division of voters in those who vote for Democrats and those who vote for Republicans.
    The function takes in input a dictionary V containing the correspondence between voters and the likelihood for each of them for Democrats and for Republicans,
    and a dictionary E containing the correspondence between pairs of voters that have a friendship relationship on facebook and their friendship level.
    The idea of the max-flow (min-cut) algorithm is applied to create a division into the two sets in order to minimize the level of friendship among the two groups,
    to maximize that within each group and to maximize the total likelihood of the returned groups (given by the sum over all voters v of the likelihood that v votes for the
    candidate of the group at which it is assigned.
    After creating a network flow suitably to solve the problem, while there is a path from the source to the destination, the value of forward edges
    is decreased considering the bottleneck of the path found and the value of backword edges is increased considering the bottleneck of the path found.
    When there are no more paths from source to destination the two sets are created considering that the voters reachable from the super Source must stay
    in the same set of super source (Democrats) and the other in the same set of super target (Republicans).
    It returns the set of Democrats and Republicans obviously excluding the super source and the super target from the sets."""

    democrats = []  # voters who vote for Democrats
    republicans = []  # voters who vote for Republicans
    netFlow, vertices, superSorg, superTarg = create_directed_graph(V, E)  # create the network flow
    path, bottleneck = define_path(netFlow, superSorg, superTarg)  # searching the first path between the source to the destination

    while len(path) > 1:  # while there is a path between the source to the destination
        for edge in path:
            edge.changeElement(edge.element() - bottleneck)  # the element associated with an edge contained into the path is decreased of the bottleneck of the path
            back = netFlow.get_edge(edge.endpoints()[1], edge.endpoints()[0])  # the "backword" edge of that found in the path
            if back is not None:  # if the "backword" edge exists
                back.changeElement(back.element() + bottleneck)  # the element associated to the "backword" edge is increased of the bottleneck of the path
            else:  # if the "backword" edge does not exist
                netFlow.insert_edge(edge.endpoints()[1], edge.endpoints()[0], bottleneck)  # the "backword" edge is inserted with an element associated equal to the bottleneck of the path
        path, bottleneck = define_path(netFlow, superSorg, superTarg)  # search a path

    reachableNode = {}
    BFSclassic(netFlow, superSorg, reachableNode)
    for democrat in reachableNode:  # vertex reachable from the source must be in Democrats
        if democrat != superSorg:
            democrats.append(democrat.element())
    for elem in netFlow.vertices():
        if elem.element() not in democrats and elem != superSorg and elem != superTarg:  # vertex not reachable from the source must be in Republicans
            republicans.append(elem.element())

    return democrats, republicans
