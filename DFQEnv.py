import random
import networkx as nx

class DFQEnv:
	def __init__(self, graph):
		self.set_graph(graph)
		set_node_attributes
		self.node
	
	def set_graph(self, graph):
		for node in graph.nodes: # Ensure the graph has all the needed information
			assert 'leakage' in graph.nodes[node]
			assert type(graph.nodes[node]['leakage']) == float
			assert 0 <= graph.nodes[node]['leakage'] <= 1
			assert 'first_name' in graph.nodes[node]
			assert type(graph.nodes[node]['first_name']) == str
			assert 'last_name' in graph.nodes[node]
			assert type(graph.nodes[node]['last_name']) == str
		self.graph = graph

	def update(self):
		