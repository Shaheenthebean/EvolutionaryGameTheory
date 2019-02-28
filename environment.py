from random import choice

class Environment:
    def __init__(self,nodes, w, mutation_rate, payoff_matrix):
        self.nodes = nodes
        self.w = w
        self.mutation_rate = mutation_rate
        self.payoff_matrix = payoff_matrix
        self.u = u

    def fitness(self, node):
        payoff = 0
        for neighbor in node.neighbors:
            payoff += self.payoff_matrix[node.strategy][neighbor.strategy]
        return 1 + self.w * payoff

    def selectNode(self):
        return choice(nodes)

    def rebirth(node):
        parent = self.select_parent()
        node.last_name = parent.last_name
        mutate = random.random()
        if mutate<self.mutation_rate:
            pass ##change to random strategy
        else:
            pass ##change to parent's strategy

    def select_parent(self): # Still to do
        node_list = []
        total_fitness = 0
        for node_i in nodes:
            node_list += [nodes[node_id].getStrategy()] * self.fitness(nodes[node_id])
            print([self.fitness(nodes[node_id]),nodes[node_id].getStrategy()])
            total_fitness += self.fitness(nodes[node_id])
        return choice(node_list)

    def update(self):
        replaced = self.selectNode()
        self.rebirth(replaced)

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
