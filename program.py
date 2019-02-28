from node import *
from environment import *

sugma=2.2
mat = [[1,2],[3,4]]
g=nx.Graph()
n_nodes = 10
for i in range(n_nodes):
    g.add_edge(i, (i + 1) % n_nodes)
e = Environment(0.05,0.05,[[1,2],[3,4]],g)

t = []
for j in range(100):
    for i in range(10000):
        e.update()


    strats = [n.strategy for n in e.nodes]
    t.append(int(strats.count(1)>strats.count(0)))


print(t.count(1))
