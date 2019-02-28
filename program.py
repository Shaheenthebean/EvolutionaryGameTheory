from environment import *

a, b, c, d = 1, 2, 3, 4
payoff_matrix = {'A': {'A': a, 'B', b}, 'A': {'A': c, 'B', d}}

# Make graph
n = 10
node_ids = range(n)
edges = [(i, (i+1) % n) for node in node_ids]
first_names, last_names = random_names(node_ids)
strategies = balanced_strategies(node_ids) # alternatively, use random_strategies
graph = make_graph(node_ids, edges, strategies, first_names, last_names)
# graph = make_graph(sample_node_ids, sample_edges, sample_strategies, sample_first_names, sample_last_names)

env = Environment(graph, payoff_matrix=payoff_matrix, mutation_rate=0.05, w=0.05)
