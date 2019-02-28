from random import choice
import node

class Environment:
    def __init__(self,nodes, w, mutation_rate, payoff_matrix):
        self.nodes = nodes
        self.w = w
        self.mutation_rate = mutation_rate
        self.payoff_matrix = payoff_matrix

    def fitness(self, node):
        payoff = 0
        for neighbor in node.neighbors:
            payoff += self.payoff_matrix[node.strategy][neighbor.strategy]
        return 1 + self.w * payoff

    def select_node(self): # Randomly selects node
        return choice(nodes)

    def rebirth(node):
        parent = self.select_parent()
        node.last_name = parent.last_name
        mutate = random.random()
        if mutate < self.mutation_rate:
            node.change_strategy(self.select_node().get_strategy()) # Change to random strategy
        else:
            node.change_strategy(self.select_parent()) # Change to parent's strategy

    def select_parent(self): # Still to do
        node_list = []
        for node_i in nodes:
            node_list += [nodes[node_id].get_strategy()] * self.fitness(nodes[node_id])
            print([self.fitness(nodes[node_id]),nodes[node_id].get_strategy()])
        return choice(node_list)

    def update(self): # Moves the environment onto the next time
        replaced = self.select_node()
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