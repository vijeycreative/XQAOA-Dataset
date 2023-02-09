import numpy as np
from numpy import sin, cos
from Graph import Graph


class XQAOA:
    def __init__(self, graph: Graph):
        """
        An XQAOA ansatz datastructure that contain five fields:
            -- graph  - A Graph object that contains the graph whose Maximum Cut we want to find.
            -- alphas - A Dict of Alpha angles. The key represents the node_id and the value 
                        respresents its corresponding alpha angle.
            -- betas  - A Dict of Beta angles. The key represents the node_id and the value 
                       respresents its corresponding beta angle.
            -- gammas -  A Dict of Gamma angles. The key represents the edge_id and the value 
                       respresents its corresponding gamma angle.
            -- edge_costs - A Dict of costs corresponding to each edge. The key represents the 
                            edge_id and the value respresents its corresponding cost.

        The order of the alphas, betas, gammas, and edge_costs dictionary follows the same order
        as those in the Graph datastructure. 
    """
        self.graph = graph
        self.alphas = {node_id: 0.0 for node_id in graph.nodes.keys()}
        self.betas = {node_id: 0.0 for node_id in graph.nodes.keys()}
        self.gammas = {edge_id: 0.0 for edge_id in graph.edges.keys()}
        self.edge_costs = {edge_id: 0.0 for edge_id in graph.edges.keys()}

    def set_angles(self, angles):
        """
            Given a input array of angles, the function first checks if the correct number of angles
            are passed. If so, it then assigns those angles to the respective nodes and edges.
        """
        assert len(angles) == 2*self.graph.num_nodes + self.graph.num_edges, "Number of angles passed is not equal to " \
                                                                           "2 * Num_Nodes + Num_Edges."
        alphas = angles[:self.graph.num_nodes]
        betas = angles[self.graph.num_nodes:2*self.graph.num_nodes]
        gammas = angles[2*self.graph.num_nodes:]

        for i, node_id in enumerate(self.alphas):
            self.alphas[node_id] = alphas[i]
        for i, node_id in enumerate(self.betas):
            self.betas[node_id] = betas[i]
        for i, edge_id in enumerate(self.gammas):
            self.gammas[edge_id] = gammas[i]

    @staticmethod
    def get_edge_id(u_id: str, v_id: str):
        """
            Given two node_ids 'u_id' and 'v_id', this function will output an edge_id string
            that follows the convention mentioned in the Graph.py file.
        """
        u_id = int(u_id)
        v_id = int(v_id)
        assert u_id != v_id, "U_ID must not be equal to V_ID"
        if u_id < v_id:
            edge_id = f"{u_id}#{v_id}"
        else:
            edge_id = f"{v_id}#{u_id}"
        return edge_id

    
    def term1(self, edge_id: str):
        """
            Given an edge_id this function computes the terms in the first line of the square 
            bracket from Equation (22) of the XQAOA paper.
        """
        u_id, v_id = edge_id.split('#')
        alpha_u = self.alphas[u_id]
        alpha_v = self.alphas[v_id]
        beta_u = self.betas[u_id]
        beta_v = self.betas[v_id]
        gamma_uv = self.gammas[edge_id]

        # e is the set of vertices other than u that are connected to v.
        e = self.graph.neighbours(v_id)
        e.remove(u_id)
        # d is the set of vertices other than v that are connected to u.
        d = self.graph.neighbours(u_id)
        d.remove(v_id)

        e_terms = cos(2 * beta_u) * sin(2 * beta_v)
        for w_id in e:
            wv_id = self.get_edge_id(w_id, v_id)
            gamma_wv = self.gammas[wv_id]
            e_terms = e_terms * cos(gamma_wv)

        d_terms = sin(2 * beta_u) * cos(2 * beta_v)
        for w_id in d:
            uw_id = self.get_edge_id(u_id, w_id)
            gamma_uw = self.gammas[uw_id]
            d_terms = d_terms * cos(gamma_uw)

        term1_total = cos(2 * alpha_u) * cos(2 * alpha_v) * sin(gamma_uv) * (e_terms + d_terms)

        return term1_total

    
    def term2(self, edge_id: str):
        """
            Given an edge_id this function computes the terms in the second line
            bracket from Equation (22) of the XQAOA paper.
        """
        u_id, v_id = edge_id.split('#')
        alpha_u = self.alphas[u_id]
        alpha_v = self.alphas[v_id]
        # triangle_nodes_id here simply the same as the set F as defined in the paper.
        triangle_nodes_id = self.graph.triangle_nodes(edge_id)
        num_triangles = len(triangle_nodes_id)

        e = self.graph.neighbours(v_id)
        e.remove(u_id)
        # e_edges_non_triangle here is simply w in e, w not in F as per the notation in equation 22 of the paper.
        e_edges_non_triangle = [self.get_edge_id(v_id, w_id) for w_id in e if w_id not in triangle_nodes_id]

        d = self.graph.neighbours(u_id)
        d.remove(v_id)
        # d_edges_non_triangle here is simply w in d, w not in F as per the notation in equation 22 of the paper.
        d_edges_non_triangle = [self.get_edge_id(u_id, w_id) for w_id in d if w_id not in triangle_nodes_id]

        E =  e_edges_non_triangle + d_edges_non_triangle
        E = list(set(E))

        term2_contributions = -0.5 * sin(2 * alpha_u) * sin(2 * alpha_v)
        for E_edge in E:
            term2_contributions = term2_contributions * cos(self.gammas[E_edge])

        triangle_1_terms = 1
        triangle_2_terms = 1

        for f_id in triangle_nodes_id:
            edge_uf_id = self.get_edge_id(u_id, f_id)
            edge_vf_id = self.get_edge_id(v_id, f_id)
            gamma_uf = self.gammas[edge_uf_id]
            gamma_vf = self.gammas[edge_vf_id]

            triangle_1_terms = triangle_1_terms * cos(gamma_uf + gamma_vf)
            triangle_2_terms = triangle_2_terms * cos(gamma_uf - gamma_vf)

        term2_total = term2_contributions * (triangle_1_terms + triangle_2_terms)

        return term2_total


    def term3(self, edge_id: str):
        """
            Given an edge_id this function computes the terms in the third line
            bracket from Equation (22) of the XQAOA paper.

            Note that the term2 and term3 functions are similar with the only 
            difference being in term3_contributions and the difference between 
            the triangle_terms. For the sake of clarity we have left term2 and 
            term3 as two separate functions.
        """
        u_id, v_id = edge_id.split('#')
        alpha_u = self.alphas[u_id]
        alpha_v = self.alphas[v_id]
        beta_u = self.betas[u_id]
        beta_v = self.betas[v_id]
        triangle_nodes_id = self.graph.triangle_nodes(edge_id)
        num_triangles = len(triangle_nodes_id)

        e = self.graph.neighbours(v_id)
        e.remove(u_id)
        e_edges_non_triangle = [self.get_edge_id(v_id, w_id) for w_id in e if w_id not in triangle_nodes_id]

        d = self.graph.neighbours(u_id)
        d.remove(v_id)
        d_edges_non_triangle = [self.get_edge_id(u_id, w_id) for w_id in d if w_id not in triangle_nodes_id]

        E =  e_edges_non_triangle + d_edges_non_triangle
        E = list(set(E))

        term3_contributions = 0.5 * cos(2 * alpha_u) * sin(2 * beta_u) * cos(2 * alpha_v) * sin(2 * beta_v)
        for E_edge in E:
            term3_contributions = term3_contributions * cos(self.gammas[E_edge])

        triangle_1_terms = 1
        triangle_2_terms = 1

        for f_id in triangle_nodes_id:
            edge_uf_id = self.get_edge_id(u_id, f_id)
            edge_vf_id = self.get_edge_id(v_id, f_id)
            gamma_uf = self.gammas[edge_uf_id]
            gamma_vf = self.gammas[edge_vf_id]

            triangle_1_terms = triangle_1_terms * cos(gamma_uf + gamma_vf)
            triangle_2_terms = triangle_2_terms * cos(gamma_uf - gamma_vf)

        term3_total = term3_contributions * (triangle_1_terms - triangle_2_terms)

        return term3_total

    
    def total_cost(self):
        """
            Computes the expectation of the optimal cut for the XQAOA ansatz.
        """

        for edge_id in self.edge_costs.keys():
            edge_in_triangle = self.graph.in_triangle(edge_id)
            term1_cost = self.term1(edge_id)
            term2_cost = self.term2(edge_id)
            if edge_in_triangle:
                term3_cost = self.term3(edge_id)
            else:
                # Term 3 doesn't contribute when it's not
                # contained in a triangle.
                term3_cost = 0.0

            edge_cost = 0.5 + 0.5 * (term1_cost + term2_cost + term3_cost)
            self.edge_costs[edge_id] = edge_cost

        total_sum = sum(self.edge_costs.values())
        return total_sum