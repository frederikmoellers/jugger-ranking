class NodeNotFound(Exception):
    """
    This is thrown if a referenced node does not exist in the graph (e.. when
    adding an edge).
    """
    def __init__(self, node):
        self._node = node

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "Node '" + str(self._node) + "' does not exist in the graph!"

class Graph:
    def __init__(self, nodes = [], edges = []):
        """
        Creates a new graph.
        Paramters:
            nodes - An iterable of objects (all of which must be hashable).
            edges - An iterable of 3-tuples (source, target, weight).
        """
        self._graph = {}
        self._graph_reverse = {}
        for node in nodes:
            self.add_node(node)
        for edge in edges:
            self.add_edge(*edge)

    def add_edge(self, source, target, weight):
        """
        Adds an edge to the graph.
        If an edge already exists between the nodes, it is updated. The
        direction of the edge is A->B if the total weight of all edges A->B is
        higher than the total weight of all edges B->A and the other way
        around. If the total weight of all edges is 0, there will be an edge in
        each direction with weight 0.
        Parameters:
            source - The source of the edge.
            target - The target of the edge.
            weight - The weight of the edge (can be negative).
        """
        for node in (source, target):
            if node not in self._graph:
                raise NodeNotFound(node)
        total_weight = weight
        if target in self._graph[source]:
            total_weight += self._graph[source][target]
            if total_weight < 0:
                del self._graph[source][target]
                del self._graph_reverse[target][source]
        elif source in self._graph[target]:
            total_weight -= self._graph[target][source]
            if total_weight > 0:
                del self._graph[target][source]
                del self._graph_reverse[source][target]
        if total_weight <= 0:
            self._graph[target][source] = -total_weight
            self._graph_reverse[source][target] = -total_weight
        if total_weight >= 0:
            self._graph[source][target] = total_weight
            self._graph_reverse[target][source] = total_weight

    def add_node(self, node):
        """
        Adds a new node to the graph.
        Parameters:
            node - The node to add.
        """
        if node not in self._graph:
            self._graph[node] = {}
            self._graph_reverse[node] = {}

    def edges(self):
        """
        Returns a set of edges. Edges are 3-tuples (source, target, weight).
        """
        e = set()
        for source in self._graph:
            for target in self._graph[source]:
                e.add((source, target, self._graph[source][target]))
        return e

    def find_circles(self):
        circles = set()
        index = {}
        lowlink = {}
        current_index = 0
        stack = []

        def strongconnect(circles, index, lowlink, current_index, stack, node):
            #nonlocal circles, index, lowlink, current_index, stack
            index[node] = current_index
            lowlink[node] = current_index
            current_index += 1
            stack.append(node)
            for succ in self._graph[node]:
                if succ not in index:
                    circles, index, lowlink, current_index, stack = strongconnect(circles, index, lowlink, current_index, stack, succ)
                    lowlink[node] = min(lowlink[node], lowlink[succ])
                elif succ in stack:
                    lowlink[node] = min(lowlink[node], index[succ])
            if lowlink[node] == index[node]:
                circle = set()
                member = None
                while member != node:
                    member = stack.pop()
                    circle.add(member)
                circles.add(frozenset(circle))
            return circles, index, lowlink, current_index, stack

        for node in self._graph:
            if node not in index:
                circles, index, lowlink, current_index, stack = strongconnect(circles, index, lowlink, current_index, stack, node)
        return circles

    def nodes(self):
        """
        Returns:
            A set containing all nodes in this graph.
        """
        return set(self._graph.keys())

    def topological_sort(self):
        # TODO: This can be done more efficiently (currently V^2+E, can be done in V+E, see wikipedia)
        reverse_circle_graph = {}
        for circle in self.find_circles():
            reverse_circle_graph[circle] = set()
        circle_assignment = {}
        for node in self._graph:
            for circle in reverse_circle_graph:
                if node in circle:
                    circle_assignment[node] = circle
                    break
        for node in self._graph:
            for succ, weight in self._graph[node].items():
                if circle_assignment[node] != circle_assignment[succ]:
                    reverse_circle_graph[circle_assignment[succ]].add(circle_assignment[node])
        topological_list = []
        while reverse_circle_graph:
            # find top nodes
            top = set()
            for circle, reverse_edges in reverse_circle_graph.items():
                if not reverse_edges:
                    top.add(circle)
            for circle in top:
                del reverse_circle_graph[circle]
            for circle, reverse_edges in reverse_circle_graph.items():
                for to_remove in (top & reverse_edges):
                    reverse_edges.remove(to_remove)
            topological_list.append(top)
        return topological_list
