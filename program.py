from node import *
from environment import *


g=nx.Graph()
n_nodes = 10
for i in range(n_nodes):
    g.add_edge(i, (i + 1) % n_nodes)
e = Environment(0.05,0.05,[[1,2],[3,4]],g)


for i in range(100):
    e.update()
