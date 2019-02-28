import random
import networkx as nx
import numpy as np
import sys
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3") # from https://stackoverflow.com/questions/9079036/how-do-i-detect-the-python-version-at-runtime

first_names = ["Liam", "Emma", "Noah", "Olivia", "William", "Ava", "James", "Isabella", "Logan", "Sophia", "Benjamin", "Mia", "Mason", "Charlotte", "Elijah", "Amelia", "Oliver", "Evelyn", "Jacob", "Abigail", "Lucas", "Harper", "Michael", "Emily", "Alexander", "Elizabeth", "Ethan", "Avery", "Daniel", "Sofia", "Matthew", "Ella", "Aiden", "Madison", "Henry", "Scarlett", "Joseph", "Victoria", "Jackson", "Aria", "Samuel", "Grace", "Sebastian", "Chloe", "David", "Camila", "Carter", "Penelope", "Wyatt", "Riley", "Jayden", "Layla", "John", "Lillian", "Owen", "Nora", "Dylan", "Zoey", "Luke", "Mila", "Gabriel", "Aubrey", "Anthony", "Hannah", "Isaac", "Lily", "Grayson", "Addison", "Jack", "Eleanor", "Julian", "Natalie", "Levi", "Luna", "Christopher", "Savannah", "Joshua", "Brooklyn", "Andrew", "Leah", "Lincoln", "Zoe", "Mateo", "Stella", "Ryan", "Hazel", "Jaxon", "Ellie", "Nathan", "Paisley", "Aaron", "Audrey", "Isaiah", "Skylar", "Thomas", "Violet", "Charles", "Claire", "Caleb", "Bella", "Josiah", "Aurora", "Christian", "Lucy", "Hunter", "Anna", "Eli", "Samantha", "Jonathan", "Caroline", "Connor", "Genesis", "Landon", "Aaliyah", "Adrian", "Kennedy", "Asher", "Kinsley", "Cameron", "Allison", "Leo", "Maya", "Theodore", "Sarah"]
last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson", "Clark", "Rodriguez", "Lewis", "Lee", "Walker", "Hall", "Allen", "Young", "Hernandez", "King", "Wright", "Lopez", "Hill", "Scott", "Green", "Adams", "Baker", "Gonzalez", "Nelson", "Carter", "Mitchell", "Perez", "Roberts", "Turner", "Phillips", "Campbell", "Parker", "Evans", "Edwards", "Collins", "Stewart", "Sanchez", "Morris", "Rogers", "Reed", "Cook", "Morgan", "Bell", "Murphy", "Bailey", "Rivera", "Cooper", "Richardson", "Cox", "Howard", "Ward", "Torres", "Peterson", "Gray", "Ramirez", "James", "Watson", "Brooks", "Kelly", "Sanders", "Price", "Bennett", "Wood", "Barnes", "Ross", "Henderson", "Coleman", "Jenkins", "Perry", "Powell", "Long", "Patterson", "Hughes", "Flores", "Washington", "Butler", "Simmons", "Foster", "Gonzales", "Bryant", "Alexander", "Russell", "Griffin", "Diaz", "Hayes"]
possible_strategies = ['A', 'B']


def sugma_calculation(sugma,a,b,c,d):
	return sugma*a+b == c+sugma*d

class Environment:
	def __init__(self, graph, payoff_matrix, mutation_rate, w, global_parent=False):
		self.graph = graph
		self.assert_graph(graph)
		self.payoff_matrix = payoff_matrix
		self.mutation_rate = mutation_rate
		self.w = w
		self.global_parent = global_parent
		self.generation = 1


	def update(self): # Moves the environment onto the next time
		replaced = self.select_node()
		self.rebirth(replaced)
		self.generation += 1

	def run(self, generations, display=False, debug=False):
		dominances = []
		last_flip = 0
		for gen in range(generations):
			self.update()
			strategies = [self.graph.nodes[node]['strategy'] for node in self.graph.nodes]
			dominance = strategies.count(possible_strategies[0])/len(self.graph.nodes) # must have python3 for division!
			if debug and len(dominances) != 0:
				if (dominance > 0.5) != (dominances[-1] > 0.5):
					print("{}\tgens, dominance flipped at {}. A from {} to {}".format(gen-last_flip, gen, dominances[-1], dominance))
					last_flip = gen
			dominances.append(dominance)
			if display:
				self.display()

	def assert_graph(self, graph): # Ensure the graph has all the needed information
		for node in graph.nodes:
			# print(graph.nodes[node])
			assert 'strategy' in graph.nodes[node]
			assert graph.nodes[node]['strategy'] in possible_strategies
			assert 'first_name' in graph.nodes[node]
			assert type(graph.nodes[node]['first_name']) == str
			assert 'last_name' in graph.nodes[node]
			assert type(graph.nodes[node]['last_name']) == str

	def set_graph(self, graph):
		self.assert_graph(graph)
		self.graph = graph

	def __repr__(self):
		return "graph: {}, payoff: {}, w: {}, mutation: {}".format(self.graph, self.payoff_matrix, self.w, self.mutation_rate)

	def fitness(self, node):
		payoff = 0
		for neighbor in self.graph.neighbors(node):
			payoff += self.payoff_matrix[self.graph.nodes[node]['strategy']][self.graph.nodes[neighbor]['strategy']]
		f = 1 + self.w * payoff
		return max(0, f)

	def select_node(self): # Randomly selects node
		return random.choice(list(self.graph.nodes.keys()))

	def rebirth(self, node):
		parent = self.select_parent(node)
		# print(parent, type(parent))
		# print(node, type(node))
		self.graph.nodes[node]['last_name'] = self.graph.nodes[parent]['last_name']
		if random.random() < self.mutation_rate:
			self.graph.nodes[node]['strategy'] = random.choice(possible_strategies) # Change to random strategy
		else:
			self.graph.nodes[node]['strategy'] = self.graph.nodes[parent]['strategy'] # Change to parent's strategy

	def select_parent(self, node=None): # Still to do
		if self.global_parent:
			nodes = list(self.graph.nodes)
		else:
			nodes = list(self.graph.neighbors(node))
		probs = np.array(list(map(self.fitness, nodes)))
		probs = probs / sum(probs) # probability distribution sums to 1
		return np.random.choice(nodes, p=probs)

	def display(self):
		pass

def calculate_sugma(self): # This is NOT a typo # TODO: Make work
		a = self.payoff_matrix['A']['A']
		b = self.payoff_matrix['A']['B']
		c = self.payoff_matrix['B']['A']
		d = self.payoff_matrix['B']['B']
		for sugma in range(0,10,0.1):
			if sugma_calculation(sugma,a,b,c,d):
				return sugma

def make_graph(node_ids, edges, strategies, first_names, last_names):
	graph = nx.Graph()  #nx.complete_graph(5)
	graph.add_nodes_from(node_ids)
	graph.add_edges_from(edges)
	attributes = {
		node_id: {
			'strategy':		strategies[node_id],
			'first_name':	first_names[node_id],
			'last_name':	last_names[node_id]
		} for node_id in node_ids}
	# print(attributes)
	nx.set_node_attributes(graph, attributes)
	return graph

# Generate random names
def random_names(node_ids):
	node_first_names, node_last_names = {}, {}
	surname_idxs = list(range(len(last_names)))
	random.shuffle(surname_idxs)
	for i, node_id in enumerate(node_ids):
		node_first_names[node_id] = random.choice(first_names)
		if i < len(last_names):
			node_last_names[node_id] = last_names[surname_idxs[i]]
		else: # out of last names, so give up and just use numbers
			node_last_names[node_id] = "surname" + str(i)
	return node_first_names, node_last_names

def random_strategies(node_ids):
	return {node_id: random.choice(possible_strategies) for node_id in node_ids}

def balanced_strategies(node_ids):
	strategies = {}
	num_per_strat = int(len(node_ids)/len(possible_strategies))
	for i, strategy in enumerate(possible_strategies):
		for node_id in node_ids[i*num_per_strat : (i+1)*num_per_strat]:
			strategies[node_id] = strategy
	return strategies


# node_ids are unique ids for the networkx graph to index its nodes
sample_node_ids = [
	'Osher',
	'Ethan',
	'Max',
	'Shaheen',
	'X'
]

sample_edges = [
	('Ethan',	'Max'),
	('Ethan', 	'Shaheen'),
	('Osher',	'Max'),
	('Osher',	'Ethan'),
	('Max',		'X')
]

sample_first_names = {
	'Osher':	'Osher',
	'Ethan':	'Ethan',
	'Max':		'Max',
	'Shaheen':	'Shaheen',
	'X':		'X'
}

sample_last_names = {
	'Osher':	'Lerner',
	'Ethan':	'Knight',
	'Max':		'Gotts',
	'Shaheen':	'Cullen-Baratloo',
	'X':		'Box'
}

sample_strategies = {
	'Osher':	'A',
	'Ethan':	'B',
	'Max':		'A',
	'Shaheen':	'B',
	'X':		'B'
}
