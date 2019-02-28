import random
import networkx as nx
import numpy as np

first_names = ["Liam", "Emma", "Noah", "Olivia", "William", "Ava", "James", "Isabella", "Logan", "Sophia", "Benjamin", "Mia", "Mason", "Charlotte", "Elijah", "Amelia", "Oliver", "Evelyn", "Jacob", "Abigail", "Lucas", "Harper", "Michael", "Emily", "Alexander", "Elizabeth", "Ethan", "Avery", "Daniel", "Sofia", "Matthew", "Ella", "Aiden", "Madison", "Henry", "Scarlett", "Joseph", "Victoria", "Jackson", "Aria", "Samuel", "Grace", "Sebastian", "Chloe", "David", "Camila", "Carter", "Penelope", "Wyatt", "Riley", "Jayden", "Layla", "John", "Lillian", "Owen", "Nora", "Dylan", "Zoey", "Luke", "Mila", "Gabriel", "Aubrey", "Anthony", "Hannah", "Isaac", "Lily", "Grayson", "Addison", "Jack", "Eleanor", "Julian", "Natalie", "Levi", "Luna", "Christopher", "Savannah", "Joshua", "Brooklyn", "Andrew", "Leah", "Lincoln", "Zoe", "Mateo", "Stella", "Ryan", "Hazel", "Jaxon", "Ellie", "Nathan", "Paisley", "Aaron", "Audrey", "Isaiah", "Skylar", "Thomas", "Violet", "Charles", "Claire", "Caleb", "Bella", "Josiah", "Aurora", "Christian", "Lucy", "Hunter", "Anna", "Eli", "Samantha", "Jonathan", "Caroline", "Connor", "Genesis", "Landon", "Aaliyah", "Adrian", "Kennedy", "Asher", "Kinsley", "Cameron", "Allison", "Leo", "Maya", "Theodore", "Sarah"]
last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson", "Clark", "Rodriguez", "Lewis", "Lee", "Walker", "Hall", "Allen", "Young", "Hernandez", "King", "Wright", "Lopez", "Hill", "Scott", "Green", "Adams", "Baker", "Gonzalez", "Nelson", "Carter", "Mitchell", "Perez", "Roberts", "Turner", "Phillips", "Campbell", "Parker", "Evans", "Edwards", "Collins", "Stewart", "Sanchez", "Morris", "Rogers", "Reed", "Cook", "Morgan", "Bell", "Murphy", "Bailey", "Rivera", "Cooper", "Richardson", "Cox", "Howard", "Ward", "Torres", "Peterson", "Gray", "Ramirez", "James", "Watson", "Brooks", "Kelly", "Sanders", "Price", "Bennett", "Wood", "Barnes", "Ross", "Henderson", "Coleman", "Jenkins", "Perry", "Powell", "Long", "Patterson", "Hughes", "Flores", "Washington", "Butler", "Simmons", "Foster", "Gonzales", "Bryant", "Alexander", "Russell", "Griffin", "Diaz", "Hayes"]
possible_strategies = ['A', 'B']


def sugma_calculation(sugma,a,b,c,d):
	return sugma*a+b == c+sugma*d

class Environment:
	def __init__(self, graph, payoff_matrix, mutation_rate, w, global_parent=True):
		self.graph = graph
		self.assert_graph(graph)
		self.payoff_matrix = payoff_matrix
		self.mutation_rate = mutation_rate
		self.w = w
		self.global_parent = global_parent

	def assert_graph(self, graph): # Ensure the graph has all the needed information
		for node in graph.nodes:
			assert 'strategy' in graph[node]
			assert graph[node]['strategy'] in possible_strategies
			assert 'name' in graph[node]
			assert type(graph[node][name]) == str

	def __repr__(self):
		return "graph: {}, payoff: {}, w: {}, mutation: {}".format(self.graph, self.payoff_matrix, self.w, self.mutation_rate)

	def fitness(self, node):
		payoff = 0
		for neighbor in self.graph.neighbors(node):
			payoff += self.payoff_matrix[self.graph[node]['strategy']][self.graph[neighbor]['strategy']]
		f = 1 + self.w * payoff
		return max(0, f)

	def select_node(self): # Randomly selects node
		return choice(self.nodes)

	def rebirth(self, node):
		parent = self.select_parent(node)
		self.graph[node]['last_name'] = self.graph[parent]['last_name']
		if random.random() < self.mutation_rate:
			self.graph[node]['strategy'] = random.choice(possible_strategies) # Change to random strategy
		else:
			self.graph[node]['strategy'] = self.graph[parent]['strategy'] # Change to parent's strategy

	def select_parent(self): # Still to do
		if self.global_parent:
			nodes = self.nodes
		else:
			nodes = list(self.graph.neighbors(node))
		probs = np.array(list(map(self.fitness, nodes)))
		probs = probs / sum(probs) # probability distribution sums to 1
		return np.random.choice(nodes, p=probs)

	def update(self): # Moves the environment onto the next time
		replaced = self.select_node()
		self.rebirth(replaced)


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
	graph.set_node_attributes(attributes)

# Generate random names
def random_names(node_ids):
	first_names, last_names = {}, {}
	surname_idxs = list(range(len(last_names)))
	random.shuffle(surname_idxs)
	for i, node_id in enumerate(node_ids):
		first_names[node_id] = random.choice(first_names)
		if i < len(last_names):
			last_names[node_id] = last_names[surname_idxs[i]]
		else: # out of last names, so give up and just use numbers
			last_names[node_id] = "surname" + str(i)
	return first_names, last_names

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
	'Shaheen',	'Shaheen',
	'X':		'Bippity'
}

sample_last_names = {
	'Osher':	'Lerner',
	'Ethan':	'Knight',
	'Max':		'Gotts',
	'Shaheen',	'Cullen-Baratloo',
	'X':		'Bop'
}

sample_strategies = {
	'Osher':	'A',
	'Ethan':	'B',
	'Max':		'A',
	'Shaheen',	'B',
	'X':		'B'
}
