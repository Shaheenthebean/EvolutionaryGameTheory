class Environment:
    def __init__(self, nodes):
        self.nodes = nodes

    def fitness(self, payoff_matrix, node, w):
        payoff = 0
        for neighbor in node.neighbors:
            payoff += payoff_matrix[node.strategy][neighbor.strategy]
        return 1 + w * payoff

    def selectNode(self):
        return nodes[0]

    def rebirth(node):
        return node


import networkx as nx

def generateNodes(graph): # Only generates neighbors (not names or strategies)
    nodes = {graph_id: Node() for graph_id in graph.nodes}
    for graph_id in nodes:
        nodes[graph_id].neighbors = [nodes[neighbor_id] for neighbor_id in graph.neighbors(graph_id)]

def generateGraph(nodes):
    graph = nx.Graph()
    graph.add_nodes_from(range(len(nodes)))

    edges = []
    for i, node in enumerate(nodes):
        edges += [(i, nodes.index(neighbor)) for neighbor in node.neighbors]
    graph.add_edges_from(edges)

    return graph
