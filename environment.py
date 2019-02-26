import random

class Environment:
    def __init__(self, nodes, w, payoff_matrix, name, u):
        self.nodes = nodes # list of nodes
        self.w = w
        self.payoff_matrix = payoff_matrix
        self.u = u

    def fitness(self, node):
        payoff = 0
        for neighbor in node.neighbors:
            payoff += self.payoff_matrix[node.strategy][neighbor.strategy]
        return 1 + self.w * payoff

    def selectNode(self):
        return random.choice(nodes)

    def rebirth(self, node): # Still to do
        node.change_strategy()

    def select_parent(self): # Still to do
        for node_i in nodes:
            self.fitness(nodes[node_id])

    def update(self):
        replaced = self.selectNode()
        self.rebirth(replaced)
