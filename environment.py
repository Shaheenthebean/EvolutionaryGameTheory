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



def generateNodes(graph):
    nodes = []
    

def generateGraph(nodes):
    graph = nx.Graph()

    names = [node.name for node in nodes]
    graph.add_nodes_from(names)

    edges = []
    for node in nodes:
        edges += [(node.name, neighbor.name) for neighbor in node.neighbors]
    graph.add_edges_from(edges)

    return graph
