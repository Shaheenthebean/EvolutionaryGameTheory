import random


class Environment:
    def __init__(self,graph,matrix):
        self.nodes = nodes

    def fitness(self, payoff_matrix, node, w):
        payoff = 0
        for neighbor in node.neighbors:
            payoff += payoff_matrix[node.strategy][neighbor.strategy]
        return 1 + w * payoff

    def selectNode(self):
        return random.choice(nodes)

    def rebirth(node):
        node.change_strategy()


    def update(self):
        replaced = self.selectNode()
        rebirth(replaced)
