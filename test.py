import networkx as nx
import matplotlib.pyplot as plt

node_ids = [
	'Osher',
	'Ethan',
	'Max',
	'Shaheen',
	'X'
]

edges = [
	('Ethan',	'Max'),
	('Ethan', 	'Shaheen'),
	('Osher',	'Max'),
	('Osher',	'Ethan'),
	('Max',		'X')
]

graph = nx.Graph()
graph.add_nodes_from(node_ids)
graph.add_edges_from(edges)

plt.subplot(121)
plt.ion()
plt.show()
for i in range(3):
	plt.clf()
	nx.draw(graph)
	plt.draw()
	plt.pause(0.001)
	input("Press [enter] to continue.")
# plt.show()
