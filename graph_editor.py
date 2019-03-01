
# based on the following demo by furas
# https://github.com/furas/my-python-codes/tree/master/pygame/__template__/
 
import pygame
import networkx as nx
 
# === CONSTANS === (UPPER_CASE names)
 
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
 
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

COLORS = [RED, BLUE]
 
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
 
# === FUNCTIONS === (lower_case names)

def mouseover(c, event):
    dx = c.centerx - event.pos[0] # A
    dy = c.centery - event.pos[1] # B
    distance_square = dx**2 + dy**2 # C^2
    return distance_square <= CIRCLE_RADIUS**2

def build_graph(connections, colors):
    g = nx.Graph()
    g.add_edges_from(connections)
    color_ids = [COLORS.index(c) for c in colors]
    color_dict = dict(enumerate(color_ids))
    nx.set_node_attributes(g, color_dict, name='color')
    return g

def run_cmd():
    global connections, color, graph
    graph = build_graph(connections, colors)
    print(f"Graph: {graph.edges}")
 
# --- init ---
 
pygame.init()
 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_rect = screen.get_rect()
 
# - circles -

lines, circles, colors, connections = [], [], [], []
selected, graph, shift_key_held = None, None, None

def clear():
    global lines, circles, colors, selected, graph
    lines, circles, colors, connections = [], [], [], []
    selected, graph = None, None

make_circle = lambda: pygame.Rect(BLOCK_SIZE-10, BLOCK_SIZE-10, BLOCK_SIZE, BLOCK_SIZE)
master_circle = make_circle()

# --- objects ---

def connect(c1, c2):
    global lines, connections
    # connect two circles with a line segment
    points = [(c1.centerx, c1.centery), (c2.centerx, c2.centery)]
    lines.append((screen, WHITE, False, points))
    connections.append((circles.index(c1), circles.index(c2)))

def cycle_color(circle):
    global colors
    circle_ind = circles.index(circle)
    cur_color_ind = COLORS.index(colors[circle_ind])
    new_color = COLORS[(cur_color_ind + 1) % len(COLORS)]
    colors[circle_ind] = new_color

# - buttons -

run_button = Button(text="Run", pos=(350,350), command=run_cmd) # create button and assign function
clear_button = Button(text="Clear", pos=(500,350), command=clear) # create button and assign function

# - drag -
 
clicking = False
selected = None
making_new_circle = False
   
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

                if mouseover(master_circle, event):
                    selected = (selected+1 if selected is not None else 0)
                    new_circle = make_circle()
                    selected_offset_y = new_circle.y - event.pos[1]
                    selected_offset_x = new_circle.x - event.pos[0]
                    making_new_circle = True

                    circles.append(new_circle)
                    colors.append(RED)

                else:
                    for i, circle in enumerate(circles):
                        if mouseover(circle, event):
                            selected = i
                    making_new_circle = False
            clicking = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if making_new_circle or (selected is None) or shift_key_held:
                    pass
                elif mouseover(circles[selected], event):
                    cycle_color(circles[selected])
                else:
                    for circle in circles:
                        if mouseover(circle, event):
                            connect(circles[selected], circle)
                clicking, selected = False, None
               
        elif event.type == pygame.MOUSEMOTION:
            if selected is not None:
                if making_new_circle:
                    new_circle.x = event.pos[0] + selected_offset_x
                    new_circle.y = event.pos[1] + selected_offset_y
                
            if not making_new_circle and shift_key_held and clicking:
                circles[selected].x = event.pos[0] + selected_offset_x
                circles[selected].y = event.pos[1] + selected_offset_y

        # -- handle events
        clear_button.handle_event(event)
        run_button.handle_event(event)
       
    # --- draws ---
   
    screen.fill(BLACK)
 
    # button1.draw(screen)    
    clear_button.draw(screen)  
    run_button.draw(screen)  
   
    # draw rect
    pygame.draw.rect(screen, GREEN, master_circle, CIRCLE_RADIUS)
    for c, color in zip(circles, colors):
        pygame.draw.circle(screen, color, c.center, CIRCLE_RADIUS)
    
    for l in lines:
        pygame.draw.lines(*l)
       
    pygame.display.update()
 
    # --- FPS ---
    clock.tick(25)
 
# --- the end ---
 
pygame.quit()
