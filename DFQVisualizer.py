
# based on the following demo by furas
# https://github.com/furas/my-python-codes/tree/master/pygame/__template__/

import pygame
import networkx as nx
from environment import *

# === CONSTANTS === (UPPER_CASE names)

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)

RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

COLORS = [RED, BLUE]
STRAT_COLORS = {possible_strategies[0]: RED, possible_strategies[1]: BLUE}

SCREEN_WIDTH  = 600
SCREEN_HEIGHT = 400

BLOCK_SIZE = 50
CIRCLE_RADIUS = int(BLOCK_SIZE/2)
FONT_SIZE = int(CIRCLE_RADIUS*0.75)

# === CLASSES === (CamelCase names)

class Button():

	def __init__(self, text='OK', pos=(0,0), size=(100,50), command=None):
		font = pygame.font.SysFont(None, 35)
		self.text = text
		self.rect = pygame.Rect((0,0), size)

		self.image_normal = pygame.Surface(size)
		self.image_normal.fill(WHITE)
		txt_image = font.render(self.text, True, RED)
		txt_rect = txt_image.get_rect(center=self.rect.center)
		self.image_normal.blit(txt_image, txt_rect)

		self.image_hover = pygame.Surface(size)
		self.image_hover.fill(RED)
		txt_image = font.render(self.text, True, WHITE)
		txt_rect = txt_image.get_rect(center=self.rect.center)
		self.image_hover.blit(txt_image, txt_rect)

		self.rect.topleft = pos

		self.hover = False

		if command:
			self.command = command
 
	def draw(self, screen):
		if self.hover:
			screen.blit(self.image_hover, self.rect)
		else:
			screen.blit(self.image_normal, self.rect)
 
	def handle_event(self, event):
		if event.type == pygame.MOUSEMOTION:
			self.hover = self.rect.collidepoint(event.pos)
 
		if self.hover and self.command:
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					self.command()
 
# --- init ---
 
pygame.init()
 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_rect = screen.get_rect()
 
# - circles -

make_circle = lambda: pygame.Rect(BLOCK_SIZE-10, BLOCK_SIZE-10, BLOCK_SIZE, BLOCK_SIZE)

class Visualizer:

	def __init__(self, env):
		self.env = env
		self.clear()

	def clear(self):
		self.selected =  None
		self.graph = nx.Graph()
		self.env.set_graph(self.graph)

	def mouseover(self, node, event):
		assert isinstance(node, dict), "Node must be passed in as a dictionary (as self.graph.nodes[node])"
		dx = node['pos'][0] - event.pos[0] # A
		dy = node['pos'][1] - event.pos[1] # B
		distance_square = dx**2 + dy**2 # C^2
		return distance_square <= node['size']**2

	def cycle_strategy(self, node):
		ind = possible_strategies.index(node['strategy'])
		new_strat = possible_strategies[(ind + 1) % len(possible_strategies)]
		node['strategy'] = new_strat

	def update_env(self):
		self.env.update()

	def draw_directed_line(self, _source, _target, width=4):
		source, target = np.array(_source), np.array(_target)
		line = [source, target]
		pygame.draw.lines(screen, WHITE, False, line, width)
		dif_vec = target - source
		perp_vec = np.array([-dif_vec[1], dif_vec[0]])/np.linalg.norm(dif_vec)
		point1 = source + 0.7 * dif_vec
		point2 = source + (0.7 - 4*width/np.linalg.norm(dif_vec)) * dif_vec + 2 * width * perp_vec
		point3 = source + (0.7 - 4*width/np.linalg.norm(dif_vec)) * dif_vec - 2 * width * perp_vec
		triangle = [list(point1), list(point2), list(point3)]
		pygame.draw.polygon(screen, WHITE, triangle)

	def run(self):
		# - buttons -

		run_button = Button(text="Run", pos=(350,350), command=self.update_env) # create button and assign function
		clear_button = Button(text="Clear", pos=(500,350), command=self.clear) # create button and assign function
		font = pygame.font.SysFont(None, FONT_SIZE)

		master_circle_rect = make_circle()
		master_circle = {'rect': master_circle_rect, 'pos': master_circle_rect.center, 'size': CIRCLE_RADIUS, 'color': GREEN}



		# - drag -

		clicking = False
		self.selected = None
		self.mouse_pos = [0,0]
		making_new_circle = False
		shift_key_held = None

		# --- mainloop ---

		clock = pygame.time.Clock()
		is_running = True

		while is_running:
			# --- events ---

			events = pygame.event.get()
			# check if alt key held)
			for event in events:
				if event.type == pygame.KEYDOWN:
					if event.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
						shift_key_held = True
				if event.type == pygame.KEYUP:
					if event.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
						shift_key_held = False

			for event in events:

				# --- global events ---

				if event.type == pygame.QUIT:
					is_running = False

				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						is_running = False

				elif event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:

						if self.mouseover(master_circle, event):
							new_node = len(self.graph.nodes)
							self.graph.add_node(new_node)
							#(self.selected+1 if self.selected is not None else 0)
							new_circle = make_circle() # TODO: Necessary?
							
							making_new_circle = True

							pos = [event.pos[0] + int(CIRCLE_RADIUS/2), event.pos[1] + int(CIRCLE_RADIUS/2)]
							selected_offset_y = pos[1] - event.pos[1]
							selected_offset_x = pos[0] - event.pos[0]
							#[new_circle.x, new_circle.y]
							first_name, last_name = random.choice(first_names), random.choice(last_names)
							nx.set_node_attributes(self.graph, {new_node: {
								'quantity': 0, 'leakage': 0}})
							self.selected = self.graph.nodes[new_node]

						else:
							for node in self.graph.nodes.values():
								if self.mouseover(node, event):
									self.selected = node
							making_new_circle = False
					clicking = True

				elif event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:
						if making_new_circle or (self.selected is None) or shift_key_held:
							pass
						elif self.mouseover(self.selected, event):
							self.selected['quantity'] += 1
						else:
							for node in self.graph.nodes.values():
								if self.mouseover(node, event):
									self.graph.add_edge(self.selected['id'], node['id'])
									# connect(self.graph.nodes[self.selected], circle)
						clicking, self.selected = False, None

				elif event.type == pygame.MOUSEMOTION:
					if self.selected is not None:
						if making_new_circle or (shift_key_held and clicking):
							self.selected['pos'][0] = event.pos[0] + selected_offset_x
							self.selected['pos'][1] = event.pos[1] + selected_offset_y
					self.mouse_pos = event.pos

				# -- handle events
				clear_button.handle_event(event)
				run_button.handle_event(event)
			
			# --- draws ---

			screen.fill(BLACK)

			# button1.draw(screen)
			clear_button.draw(screen)
			run_button.draw(screen)

			# draw circle generator
			pygame.draw.rect(screen, master_circle['color'], master_circle['rect'], master_circle['size'])
			# draw nodes
			for node in self.graph.nodes:
				color = STRAT_COLORS[self.graph.nodes[node]['strategy']]
				size = int(CIRCLE_RADIUS * max(0.5, self.env.fitness(node)**0.3)) # environment specific
				pygame.draw.circle(screen, color, self.graph.nodes[node]['pos'], size)
				self.graph.nodes[node]['size'] = size
				name = self.graph.nodes[node]['first_name'] + ' ' + self.graph.nodes[node]['last_name']
				text = font.render(name, True, WHITE)
				screen.blit(text, self.graph.nodes[node]['pos'])

			for edge in self.graph.edges:
				self.draw_directed_line(self.graph.nodes[edge[0]]['pos'], self.graph.nodes[edge[1]]['pos'])

			# display line while dragging
			if clicking and not making_new_circle and not shift_key_held and self.selected != None:
				self.draw_directed_line(self.selected['pos'], self.mouse_pos)

			pygame.display.update()

			# --- FPS ---
			clock.tick(25)

		# --- the end ---

		pygame.quit()

if __name__ == "__main__":
	a, b, c, d = 2, -0.5, 0.5, 1
	payoff_matrix = {'A': {'A': a, 'B': b}, 'B': {'A': c, 'B': d}}
	env = Environment(nx.DiGraph(), payoff_matrix=payoff_matrix, mutation_rate=0.05, w=1)

	vis = Visualizer(env)
	vis.run()
