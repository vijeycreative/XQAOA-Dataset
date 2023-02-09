class Node:
    """
        A Node datastructure contains two fields:
            -- node_id - An int value that is used to identify the node.
            -- neighbours - A list of node_id that are adjacent to the current node.

        The __eq__  function is used to check if the two node objects are the same 
        and the __repr__ function is used to display the object nicely when printed.
    """
    def __init__(self, node_id):
        self.nid = node_id
        self.neighbours = None

    def __eq__(self, node):
        # Check if two different vertex variables are
        # indeed the same vertex of the graph
        return self.nid == node.nid

    def __repr__(self):
        return f"Node(ID='{self.nid}')"


class Edge:
    """
        An Edge datastructure that contain five fields:
            -- eid - An int value that is used to identify the edge.
            -- u - A Node object that represents the node u.
            -- v - A Node object that represents the node v.
            -- in_triangle - A boolean value that indicates if the edge is contained in a triangle.
            -- triangle_nodes - A list of Node objects that form a triangle with the edge {u, v}.

        The __eq__  function is used to check if the two edge objects are the same 
        and the __repr__ function is used to display the object nicely when printed.

        The contains_vertex function outputs True if a given node is a part of the edge and False otherwise.
    """
    def __init__(self, edge_id, u: Node, v: Node):
        self.eid = edge_id
        self.u = u
        self.v = v
        self.in_triangle = None
        self.triangle_nodes = None

    def __repr__(self):
        return f"Edge(ID={self.eid}, U={self.u.nid}, V={self.v.nid}, Triangle_Nodes={self.triangle_nodes})"

    def __eq__(self, edge):
        # Check if two different edge variables are
        # indeed the same edge of the graph
        return self.eid == edge.eid

    def contains_vertex(self, node: Node):
        # Check if the given vertex is contained in the edge
        return (self.u == node) or (self.v == node)


class Graph:
    """
        An Graph datastructure that contain four fields:
            -- num_nodes - Total number of nodes present in the graph.
            -- num_edges - Total Number of edges present in the graph.
            -- nodes - A Dict of Node objects for all the nodes present in the graph. 
                       The node_id ranges from 0 to num_nodes-1.
            -- edges - A Dict of Edge objects for all the nodes present in the graph. 
                       Edges are sorted in ascending order of node_ids. 
    """
    def __init__(self, n: int, edges: list):

        self.num_nodes = n
        self.num_edges = len(edges)
        self.nodes = self.construct_nodes()
        self.edges = self.construct_edges(edges)

        for nid, node in self.nodes.items():
            node.neighbours = self.neighbours(nid)

        for eid, edge in self.edges.items():
            edge.triangle_nodes = self.triangle_nodes(eid)
            edge.in_triangle = len(edge.triangle_nodes) != 0

    def construct_nodes(self):
        """
            Generate a dictionary and fill it with Node objects for all the 
            nodes in the graph. The node_id is the key and the Node object 
            is the value. The dictionary is populated in a sequential order, 
            starting from 0 to num_nodes-1, to enable each node to be associated 
            with its alpha and beta angles based on its index.
        """
        nodes = {}
        graph_nodes = list(range(self.num_nodes))
        for i in graph_nodes:
            nodes[f'{i}'] = Node(node_id=f'{i}')
        return nodes

    def construct_edges(self, edges_list):
        """
            Build a dictionary and fill it with Edge objects for all the edges in 
            the graph. The edge_id is used as the key and the Edge object is the 
            value. The edge_id is created using a convention where two node_ids are 
            separated by a # sign, with the smaller node_id always appearing before 
            the # symbol. The dictionary is filled with the edge_ids and Edge objects 
            in ascending order based on the node_ids in each edge_id. This specific 
            ordering of the dictionary is established to enable mapping of each edge 
            to its gamma value based on its index.
        """

        edges = {}
        graph_edges = edges_list
        graph_edges = [tuple(sorted(graph_edge)) for graph_edge in graph_edges]
        graph_edges.sort(key=lambda x: (x[0], x[1]))
        for i, j in graph_edges:
            i_node = self.nodes[f'{i}']
            j_node = self.nodes[f'{j}']
            if i < j:
                edges[f'{i}#{j}'] = Edge(edge_id=f'{i}#{j}', u=i_node, v=j_node)
            else:
                edges[f'{j}#{i}'] = Edge(edge_id=f'{j}#{i}', u=j_node, v=i_node)
        return edges

    def neighbours(self, node_id: str):
        """
            Given a node n, this function returns a set of nodes that are
            adjacent to the node n in the graph.
        """
        neighbour_list = []
        for eid in self.edges.keys():
            node1_id, node2_id = eid.split('#')
            if node_id == node1_id:
                neighbour_list.append(node2_id)
            elif node_id == node2_id:
                neighbour_list.append(node1_id)
        return set(neighbour_list)

    def triangle_nodes(self, edge_id: str):
        """
            Given a edge {u, v}, this function returns a set of nodes that form
            a triangle with the edge {u, v} in the graph.
        """
        u_id, v_id = edge_id.split('#')
        u_neighbours_id = self.neighbours(u_id)
        v_neighbours_id = self.neighbours(v_id)
        triangle_nodes_id = u_neighbours_id.intersection(v_neighbours_id)
        return triangle_nodes_id

    def in_triangle(self, edge_id: str):
        """
            Given a edge {u, v}, this function returns True if the edge is 
            contained in a graph and false otherwise. 
        """
        return len(self.triangle_nodes(edge_id)) != 0
