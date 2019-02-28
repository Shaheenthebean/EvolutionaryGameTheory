from node import *
from environment import *

mat = [[1,2],[-5,4]]
g=nx.Graph()
n_nodes = 100
sugma = (3*n_nodes-8)/n_nodes
print(sugma*mat[0][0]+mat[0][1])
print(mat[1][0]+sugma*mat[1][1])
for i in range(n_nodes):
    g.add_edge(i, (i + 1) % n_nodes)
e = Environment(0.0050,0.005,mat,g)

t = []
for j in range(100):
    for i in range(100000):
        e.update()


    strats = [n.strategy for n in e.nodes]
    t.append(int(strats.count(1)>strats.count(0)))


print(t.count(1))
