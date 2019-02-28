from random import *
from node import *
import networkx as nx

first_names = ["Liam", "Emma", "Noah", "Olivia", "William", "Ava", "James", "Isabella", "Logan", "Sophia", "Benjamin", "Mia", "Mason", "Charlotte", "Elijah", "Amelia", "Oliver", "Evelyn", "Jacob", "Abigail", "Lucas", "Harper", "Michael", "Emily", "Alexander", "Elizabeth", "Ethan", "Avery", "Daniel", "Sofia", "Matthew", "Ella", "Aiden", "Madison", "Henry", "Scarlett", "Joseph", "Victoria", "Jackson", "Aria", "Samuel", "Grace", "Sebastian", "Chloe", "David", "Camila", "Carter", "Penelope", "Wyatt", "Riley", "Jayden", "Layla", "John", "Lillian", "Owen", "Nora", "Dylan", "Zoey", "Luke", "Mila", "Gabriel", "Aubrey", "Anthony", "Hannah", "Isaac", "Lily", "Grayson", "Addison", "Jack", "Eleanor", "Julian", "Natalie", "Levi", "Luna", "Christopher", "Savannah", "Joshua", "Brooklyn", "Andrew", "Leah", "Lincoln", "Zoe", "Mateo", "Stella", "Ryan", "Hazel", "Jaxon", "Ellie", "Nathan", "Paisley", "Aaron", "Audrey", "Isaiah", "Skylar", "Thomas", "Violet", "Charles", "Claire", "Caleb", "Bella", "Josiah", "Aurora", "Christian", "Lucy", "Hunter", "Anna", "Eli", "Samantha", "Jonathan", "Caroline", "Connor", "Genesis", "Landon", "Aaliyah", "Adrian", "Kennedy", "Asher", "Kinsley", "Cameron", "Allison", "Leo", "Maya", "Theodore", "Sarah"]
last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson", "Clark", "Rodriguez", "Lewis", "Lee", "Walker", "Hall", "Allen", "Young", "Hernandez", "King", "Wright", "Lopez", "Hill", "Scott", "Green", "Adams", "Baker", "Gonzalez", "Nelson", "Carter", "Mitchell", "Perez", "Roberts", "Turner", "Phillips", "Campbell", "Parker", "Evans", "Edwards", "Collins", "Stewart", "Sanchez", "Morris", "Rogers", "Reed", "Cook", "Morgan", "Bell", "Murphy", "Bailey", "Rivera", "Cooper", "Richardson", "Cox", "Howard", "Ward", "Torres", "Peterson", "Gray", "Ramirez", "James", "Watson", "Brooks", "Kelly", "Sanders", "Price", "Bennett", "Wood", "Barnes", "Ross", "Henderson", "Coleman", "Jenkins", "Perry", "Powell", "Long", "Patterson", "Hughes", "Flores", "Washington", "Butler", "Simmons", "Foster", "Gonzales", "Bryant", "Alexander", "Russell", "Griffin", "Diaz", "Hayes"]

class Environment:
	def __init__(self, w, mutation_rate, payoff_matrix, nx_graph):
		self.initialize_nodes(nx_graph)
		self.w = w
		self.mutation_rate = mutation_rate
		self.payoff_matrix = payoff_matrix
		self.graph = None

	def __repr__(self):
		return [self.graph, self.nodes]

	def fitness(self, node):
		payoff = 0
		for neighbor in node.neighbors:
			payoff += self.payoff_matrix[node.strategy][neighbor.strategy]
		return 1 + self.w * payoff

	def select_node(self): # Randomly selects node
		return random.choice(nodes)

	def rebirth(self, node):
		parent = self.select_parent()
		node.last_name = parent.last_name
		mutate = random.random()
		if mutate < self.mutation_rate:
			node.change_strategy(choice([0,1])) # Change to random strategy
		else:
			node.change_strategy(parent.strategy) # Change to parent's strategy

	def select_parent(self): # Still to do
		node_list = []
		for node_i in nodes:
			node_list += [nodes[node_id].get_strategy()] * self.fitness(nodes[node_id])
			print([self.fitness(nodes[node_id]),nodes[node_id].get_strategy()])
		return random.choice(node_list)

	def update(self): # Moves the environment onto the next time
		replaced = self.select_node()
		self.rebirth(replaced)

	def initialize_nodes(self, graph): # Only generates neighbors (not names or strategies)
        # Connect nodes
		nodes = {graph_id: Node() for graph_id in graph.nodes}
		for graph_id in nodes:
			nodes[graph_id].neighbors = [nodes[neighbor_id] for neighbor_id in graph.neighbors(graph_id)]
        self.nodes = list(nodes.values())
        # TODO: Generate names
        surname_idxs = list(range(len(last_names)))
        random.shuffle(surname_idxs)
        for i, node in enumerate(self.nodes):
            if i < len(last_names):
                node.last_name = last_names[surname_idxs[i]]
            else:
                node.last_name = str(i)
            node.first_name = random.choice(first_names)
        # TODO: Set strategies

	def generate_raph(self):
		graph = nx.Graph()
		graph.add_nodes_from(range(len(self.nodes)))

		edges = []
		for i, node in enumerate(self.nodes):
			edges += [(i, self.nodes.index(neighbor)) for neighbor in node.neighbors]
		graph.add_edges_from(edges)

		return graph
