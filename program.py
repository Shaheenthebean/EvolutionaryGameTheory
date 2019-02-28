from environment import *

a, b, c, d = 1, 2, -5, 4
payoff_matrix = {'A': {'A': a, 'B', b}, 'A': {'A': c, 'B', d}}

# Make graph
n_nodes = 10
node_ids = range(n_nodes)
edges = [(i, (i+1) % n) for node in node_ids]
first_names, last_names = random_names(node_ids)
strategies = balanced_strategies(node_ids) # alternatively, use random_strategies
graph = make_graph(node_ids, edges, strategies, first_names, last_names)
# graph = make_graph(sample_node_ids, sample_edges, sample_strategies, sample_first_names, sample_last_names)
sugma = (3*n_nodes-8)/n_nodes
print(sugma*a + b)
print(c + sugma*d)

env = Environment(graph, payoff_matrix=payoff_matrix, mutation_rate=0.05, w=0.05)

t = []
for j in range(100):
    for i in range(100000):
        env.update()


    strats = [env[n]['strategy'] for n in env.nodes]
    t.append(strats.count('A') > strats.count('B'))


print(t.count(True))
