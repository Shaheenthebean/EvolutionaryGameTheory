import random


class Environment:
    def __init__(self,nodes, w, payoff_matrix):
        self.nodes = nodes
        self.w = w
        self.payoff_matrix = payoff_matrix

    def fitness(self, node):
        payoff = 0
        for neighbor in node.neighbors:
            payoff += self.payoff_matrix[node.strategy][neighbor.strategy]
        return 1 + self.w * payoff

    def selectNode(self):
        return random.choice(nodes)

    def rebirth(node):
        node.change_strategy()


    def update(self):
        replaced = self.selectNode()
        rebirth(replaced)
