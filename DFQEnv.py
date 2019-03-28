import random
import networkx as nx

class DFQEnv:
	def __init__(self, graph):
		self.set_graph(graph)
		# nx.set_node_attributes(self.graph)
		# self.node
	
	def set_graph(self, graph):
		for node in graph.nodes: # Ensure the graph has all the needed information
			if node != "Garbage":
				assert 'leakage' in graph.nodes[node]
				assert type(graph.nodes[node]['leakage']) == float
				assert 0 <= graph.nodes[node]['leakage'] <= 1
			assert 'quantity' in graph.nodes[node]
			assert type(graph.nodes[node]['quantity']) == float or type(graph.nodes[node]['quantity']) == int
			assert 0 <= graph.nodes[node]['quantity']
		self.graph = graph

	def update(self):
		pass