import random


class Environment:
    def __init__(self,nodes):
        self.nodes = nodes

    def fitness(self, payoff_matrix, node, w):
        payoff = 0
        for neighbor in node.neighbors:
            payoff += payoff_matrix[node.strategy][neighbor.strategy]
        return 1 + w * payoff

    def selectNode(self):
        return random.choice(nodes)

    def rebirth(self,node):
        return node

    def update(self):
        replaced = self.selectNode()
        rebirth(replaced)
