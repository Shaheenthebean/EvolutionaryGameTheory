

class Organism:
    def __init__(self):
        self.neighbors = []
        pass

    def add_neighbor(self,neighbor):
        self.neighbors.append(neighbor)



def make_neighbors(org1, org2):
    org1.add_neighbor(org2)
    org2.add_neighbor(org1)
