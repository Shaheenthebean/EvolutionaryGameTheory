
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

	def __init__(self):
		self.clear()

	def clear(self):
		self.selected =  None
		self.graph = nx.Graph()

	def mouseover(self, node, event):
		assert isinstance(node, dict), "Node must be passed in as a dictionary (as self.graph.nodes[node])"
		dx = node['pos'][0] - event.pos[0] # A
		dy = node['pos'][1] - event.pos[1] # B
		distance_square = dx**2 + dy**2 # C^2
		return distance_square <= node['size']**2

	def cycle_strategy(self, node):
		ind = possible_strategies.index(node['strategy'])
		new_strat = possible_strategies[(strat_ind + 1) % len(possible_strategies)]
		node['strategy'] = new_strat

	def run(self):
		# - buttons -

		run_button = Button(text="Run", pos=(350,350), command=run_cmd) # create button and assign function
		clear_button = Button(text="Clear", pos=(500,350), command=clear) # create button and assign function
		master_circle = {'rect': make_circle(), 'size': CIRCLE_RADIUS, 'color': GREEN}


		# - drag -
		
		clicking = False
		self.selected = None
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
							selected_offset_y = new_circle.y - event.pos[1]
							selected_offset_x = new_circle.x - event.pos[0]
							making_new_circle = True

							pos = (new_circle.centerx, new_circle.center_y)
							first_name, last_name = random.choice(first_names), random.choice(last_names)
							nx.set_node_attributes(self.graph, {new_node: {
								'pos': pos, 'strategy': possible_strategies[0], 'id': new_node,
								'first_name': first_name, 'last_name': last_name}})
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
							self.cycle_strategy(self.selected)
						else:
							for node in self.graph.nodes.values():
								if mouseover(node, event):
									self.graph.add_edge(self.selected['id'], node['id'])
									# connect(self.graph.nodes[self.selected], circle)
						clicking, self.selected = False, None
					
				elif event.type == pygame.MOUSEMOTION:
					if self.selected is not None:
						if making_new_circle or (shift_key_held and clicking):
							self.selected['pos'][0] = event.pos[0] + selected_offset_x
							self.selected['pos'][1] = event.pos[1] + selected_offset_y

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
			for node in self.graph.nodes.values():
				color = STRAT_COLORS[node['strategy']]
				size = CIRCLE_RADIUS * max(0.5, env.fitness(node))
				pygame.draw.circle(screen, color, node['pos'], size)

			for edge in self.graph.edges:
				line = [self.graph.nodes[edge[0]]['pos'], self.graph.nodes[edge[1]]['pos']]
				pygame.draw.lines(screen, WHITE, False, line)

			pygame.display.update()
		
			# --- FPS ---
			clock.tick(25)
		
		# --- the end ---
		
		pygame.quit()
