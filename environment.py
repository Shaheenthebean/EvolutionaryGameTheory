from random import choice
from node import *
import networkx as nx

class Environment:
	def __init__(self, w, mutation_rate, payoff_matrix, nx_graph):
		self.initialize_nodes(nx_graph)
		self.w = w
		self.mutation_rate = mutation_rate
		self.payoff_matrix = payoff_matrix
		self.graph = None

	def __repr__(self):
		return [self.graph, self.nodes]

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

	def initialize_nodes(self, graph): # Only generates neighbors (not names or strategies)
        # Connect nodes
		nodes = {graph_id: Node() for graph_id in graph.nodes}
		for graph_id in nodes:
			nodes[graph_id].neighbors = [nodes[neighbor_id] for neighbor_id in graph.neighbors(graph_id)]
        self.nodes = list(nodes.values())
        # TODO: Generate names
        # TODO: Set strategies

	def generate_raph(self):
		graph = nx.Graph()
		graph.add_nodes_from(range(len(self.nodes)))

		edges = []
		for i, node in enumerate(self.nodes):
			edges += [(i, self.nodes.index(neighbor)) for neighbor in node.neighbors]
		graph.add_edges_from(edges)

		return graph


