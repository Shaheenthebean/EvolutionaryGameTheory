import random


class Environment:
    def __init__(self,nodes, w, mutation_rate, payoff_matrix):
        self.nodes = nodes
        self.w = w
        self.mutation_rate = mutation_rate
        self.payoff_matrix = payoff_matrix

    def fitness(self, node):
        payoff = 0
        for neighbor in node.neighbors:
            payoff += self.payoff_matrix[node.strategy][neighbor.strategy]
        return 1 + self.w * payoff

    def selectNode(self):
        return random.choice(nodes)

    def rebirth(node):
        parent = self.select_parent()
        node.last_name = parent.last_name
        mutate = random.random()
        if mutate<self.mutation_rate:
            pass ##change to random strategy
        else:
            pass ##change to parent's strategy


    def update(self):
        replaced = self.selectNode()
        rebirth(replaced)
