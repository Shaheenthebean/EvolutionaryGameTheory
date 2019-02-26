

class Node:
    def __init__(self, strategy, first_name,last_name):
        self.strategy = strategy
        self.first_name = first_name
        self.last_name = last_name
        self.neighbors = []

    def add_neighbor(self,neighbor):
        self.neighbors.append(neighbor)



def make_neighbors(org1, org2):
    org1.add_neighbor(org2)
    org2.add_neighbor(org1)
