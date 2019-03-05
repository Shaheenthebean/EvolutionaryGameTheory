from environment import Environment
from visualizer import Visualizer

a, b, c, d = 2, -0.5, 0.5, 1
payoff_matrix = {'A': {'A': a, 'B': b}, 'B': {'A': c, 'B': d}}
env = Environment(nx.Graph(), payoff_matrix=payoff_matrix, mutation_rate=0.05, w=1)

vis = Visualizer(env)
vis.run()
