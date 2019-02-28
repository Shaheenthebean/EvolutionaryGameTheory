from environment import *

a, b, c, d = 1, 2, -5, 4
payoff_matrix = {'A': {'A': a, 'B': b}, 'B': {'A': c, 'B': d}}

# Make graph
n_nodes = 100
node_ids = range(n_nodes)
edges = [(node, (node+1) % n_nodes) for node in node_ids]
first_names, last_names = random_names(node_ids)
strategies = balanced_strategies(node_ids) # alternatively, use random_strategies
graph = make_graph(node_ids, edges, strategies, first_names, last_names)
# graph = make_graph(sample_node_ids, sample_edges, sample_strategies, sample_first_names, sample_last_names)
sugma = (3*n_nodes-8)/n_nodes
print(sugma*a + b)
print(c + sugma*d)

env = Environment(graph, payoff_matrix=payoff_matrix, mutation_rate=0.05, w=0.05)

t = []
iterations = 100
for j in range(iterations):
	for i in range(10000):
		env.update()


	strats = [env.graph.nodes[node]['strategy'] for node in env.graph.nodes]
	a_dom = strats.count('A') > strats.count('B')
	# print(j, a_dom)
	t.append(a_dom)


print(t.count(True)/float(iterations)*100,"%")
