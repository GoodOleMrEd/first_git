import sys, pygame,time, random
from pygame.locals import *

BLACK = (0,0,0)
BROWN = (153,76,0)
GREEN = (0, 255, 0)
BLUE = (0,0,255)
RED = (255,0,0)
GREY = (200,200,200)

WHITE = (255,255,255)
BRIGHTBLUE = (0,50, 255)
DARKTURQUOISE =(3,54,73)
GREEN = (0, 204,0)

DIRT = 0
GRASS = 1
WATER = 2
COAL = 3

RESOURCES = ['DIRT', 'GRASS', 'WATER', 'LAVA', 'DIAMOND']
TEXTURES = {'DIRT':pygame.image.load('images/land.png'), 'GRASS':pygame.image.load('images/grass.png'), 'WATER':pygame.image.load('images/water.png'), 'LAVA':pygame.image.load('images/lava.png'), 'DIAMOND':pygame.image.load('images/diamond.png')}

class Enemy():
	def __init__(self, screen, game_settings, tile_map):
		self.screen = screen
		self.game_settings = game_settings
		self.tile_map = tile_map
		self.filename = "black_mage.png"
		self.pos = [random.randint(0,game_settings.board_width), random.randint(0,game_settings.board_height-3)]
		self.image = pygame.image.load(self.filename)
		self.rect_left = self.pos[0] * game_settings.tile_size
		self.rect_top = self.pos[1] * game_settings.tile_size

	def blit(self):
		self.screen.blit(self.image, (self.rect_left, self.rect_top))

	def move(self, hero, game_settings):
		if random.randint(1,30) == 1:
			if hero.pos[1] < self.pos[1] and self.rect_top >= 0 and self.tile_map[self.pos[0]][self.pos[1] - 1] != 'DIAMOND':
				self.pos[1] -= 1
				self.rect_top = self.pos[1] * game_settings.tile_size
			elif hero.pos[0] < self.pos[0] and self.rect_left >= 0 and self.tile_map[self.pos[0]-1][self.pos[1]] != 'DIAMOND':
				self.pos[0] -= 1
				self.rect_left = self.pos[0] * game_settings.tile_size
			elif hero.pos[1] > self.pos[1] and self.tile_map[self.pos[0]][self.pos[1] + 1] != 'DIAMOND':
				self.pos[1] += 1
				self.rect_top = self.pos[1] * game_settings.tile_size
			elif hero.pos[0] > self.pos[0] and self.tile_map[self.pos[0]+ 1][self.pos[1]] != 'DIAMOND':
				self.pos[0] += 1
				self.rect_left = self.pos[0] * game_settings.tile_size



class Player():
	def __init__(self, screen, game_settings):
		self.screen = screen
		self.screen_rect = self.screen.get_rect()
		self.filename = "images/player.png"
		self.image = pygame.image.load(self.filename)

		self.pos = [0,0]
		self.rect = self.image.get_rect()
		self.rect.left = self.pos[0] * game_settings.tile_size
		self.rect.top = self.pos[1] * game_settings.tile_size
		self.player_moving_left = False
		self.player_moving_right = True
		#self.rect.left = int(game_settings.tile_size * self.pos[0])
		#self.rect.top = int(game_settings.tile_size * self.pos[1])


	def upate_image(self):
		if self.player_moving_left:
			self.filename = 'images/player_left.png'
			self.image = pygame.image.load(self.filename)
		else:

			self.image = pygame.image.load('images/player.png')

	def blit(self, game_settings):
		self.screen.blit(self.image,self.rect)#(game_settings.tile_size * self.pos[0],game_settings.tile_size *self.pos[1]))
		
		

	def move(self, event, game_settings, inventory_button):
		if event.type == pygame.KEYDOWN:
			if event.key == K_DOWN and self.rect.top < (inventory_button.top - game_settings.tile_size*2):
				self.pos[1] += 1
				self.rect.top += game_settings.tile_size
			if event.key == K_UP and self.rect.top > 0:
				self.pos[1] -= 1
				self.rect.top -= game_settings.tile_size
			if event.key == K_RIGHT and self.pos[0] < game_settings.board_width-1:
				self.pos[0] += 1
				self.rect.right += game_settings.tile_size
				self.player_moving_right = True
				self.player_moving_left = False
			if event.key == K_LEFT and self.pos[0] > 0:
				self.pos[0] -= 1
				self.rect.left -= game_settings.tile_size
				self.player_moving_left = True
				self.player_moving_right = False



class Inventory():
	def __init__(self, player, game_settings):
		self.player = player
		self.game_settings = game_settings
		self.resources = {'DIRT':0, 'WATER':0, 'GRASS':0, 'LAVA':0, 'DIAMOND':0}

	def add_to_inventory(self, player, event, tile_map):

		current_tile = tile_map[player.pos[0]][player.pos[1]]
		if event.type == pygame.KEYDOWN:
			if event.key == K_SPACE:
				self.resources[current_tile] += 1
				
				tile_map[player.pos[0]][player.pos[1]] = 'DIRT'



class Settings():
	def __init__(self):
		self.window_width = 26*15
		self.window_height = 26*15
		self.window_color = (220,220,220)
		self.tile_size = 26
		self.board_width = int(self.window_width/self.tile_size)
		self.board_height = int(self.window_height/self.tile_size)
		self.fps = 30
		
	
		self.font_size = 20

def check_mouse_action(event, lava_icon, water_icon, grass_icon):
	selected_icon = ''
	if event.type == pygame.MOUSEBUTTONDOWN: 
		mousex,mousey = pygame.mouse.get_pos()
		if grass_icon.rect.collidepoint(mousex,mousey):
			selected_icon = 'GRASS'
		elif lava_icon.rect.collidepoint(mousex,mousey):
			selected_icon = 'LAVA'
			
		elif water_icon.rect.collidepoint(mousex, mousey):
			selected_icon = "WATER"
			
		
	print (selected_icon)
	return selected_icon

def place_selected_tile(selected_icon, inventory, event, tile_map, hero):
	item_placed = False
	if event.type == pygame.KEYDOWN and event.key == K_r:
		if selected_icon in inventory.resources:
			if inventory.resources[selected_icon] >= 1:	
				tile_map[hero.pos[0]][hero.pos[1]] = selected_icon

def decrement_inventory(selected_icon, event, inventory):
	if event.type == pygame.KEYUP and event.key == K_r and inventory.resources[selected_icon] >= 1 and selected_icon in inventory.resources:
		inventory.resources[selected_icon] -= 1	
							
def check_game_over(hero, enemy, clock):
	if hero.pos[0] == enemy.pos[0] and hero.pos[1] == enemy.pos[1]:
		time.sleep(3)
		pygame.quit()
		sys.exit()

def create_duplicate_board(tile_map):
	duplicate_board = []
	for i in tile_map:
		duplicate_board.append(i)

	return duplicate_board

def check_four_squares(tile_map, game_settings, four_tiles):
	points = 0
	duplicate_board = create_duplicate_board(tile_map)
	for x in range(1, game_settings.board_width):
		for y in range(1, game_settings.board_height):
			if duplicate_board[x][y] == duplicate_board[x+1][y] and duplicate_board[x+1][y] == duplicate_board[x+1][y-1] and duplicate_board[x][y] == duplicate_board[x][y-1]:
				points += 1
				four_tiles[x] = y
			#if duplicate_board[x][y] == duplicate_board[x-1][y] and duplicate_board[x-1][y+1] == duplicate_board[x][y] and duplicate_board[x][y+1] == duplicate_board[x][y]:
				#points += 1
				#four_tiles[x] = y
	print (points)

				
def fill_in_four_tiles(four_tiles, tile_map):
	for x,y in four_tiles.items():
		tile_map[x][y] = 'DIAMOND'
		tile_map[x+1][y] = 'DIAMOND'
		tile_map[x+1][y-1] = 'DIAMOND'
		tile_map[x][y-1] = 'DIAMOND'

	
		
		

def create_objective_tile(game_settings, tile_map):
	x_value = random.randint(1,game_settings.board_width)
	y_value = random.randint(1,game_settings.board_height-4)
	#tile_map[x_value][y_value] = pygame.draw.rect(screen, WHITE, )				

def check_exit_action(event, game_settings):
	if event.type == pygame.QUIT:
		pygame.quit()
		sys.exit()
	elif event.type == pygame.KEYDOWN:
		if event.key == K_q:
			pygame.quit()
			sys.exit()
  				
def check_if_on_lava(player, tile_map):
	if tile_map[player.pos[0]][player.pos[1]] == 'LAVA':
		print ("YOU ARE DEAD!")


def create_tile_map(game_settings):
	tile_map = []
	for x in range(game_settings.board_width + 1):
		column = []
		for y in range(game_settings.board_height + 1):
			selection = random.randint(0,10)
			if selection in (0,1,2):
				column.append("DIRT")
			elif selection in (3,4,5):
				column.append("GRASS")
			elif selection in (6,7,8):
				column.append("WATER")
			else:
				column.append("LAVA")
			#column.append(random.choice(RESOURCES))
			#column.append('WATER')
			#column.append(RESOURCES[random.randint(0,len(RESOURCES)-1)])

		tile_map.append(column)
	return tile_map

def draw_tile_map(tile_map, game_settings, screen):
	for row in range(len(tile_map)):
		for column in range(game_settings.board_height):
			screen.blit(TEXTURES[tile_map[column][row]], (column * game_settings.tile_size, row * game_settings.tile_size))


class Button():
	def __init__(self,game_settings, screen, msg):
		self.game_settings = game_settings
		self.screen = screen
		self.left = 0
		self.top = game_settings.window_height - ((game_settings.tile_size +1)*2)
		self.width = game_settings.window_width
		self.height = ((game_settings.tile_size +1)*2)
		self.font = pygame.font.SysFont(None, self.game_settings.tile_size- 5)
		self.text_color = WHITE
		self.msg = msg
		

	def draw_button(self, game_settings,screen):
		pygame.draw.rect(screen, BLACK, (self.left,self.top, self.width,self.height),self.height)
		self.msg_image = self.font.render(self.msg, True, self.text_color)
		self.screen.blit(self.msg_image,(3,self.top - 24))
			
class Icon():
	def __init__(self, game_settings, screen, x_value, texture, inventory):
		self.game_settings = game_settings
		self.screen = screen
		self.texture = texture
		self.y_value = self.game_settings.window_height - (self.game_settings.tile_size * 2)
		self.x_value = x_value * self.game_settings.tile_size
		self.text_color = WHITE
		self.font = pygame.font.SysFont(None,game_settings.tile_size)
		self.inventory = inventory
		self.rect = pygame.Rect(self.x_value,self.y_value,game_settings.tile_size, game_settings.tile_size)

	def draw_icon(self):
		self.screen.blit(TEXTURES[self.texture], (self.x_value,self.y_value))
		self.msg_image = self.font.render(str(self.inventory.resources[self.texture]), True, self.text_color)
		self.msg_image_rect = (self.x_value + self.game_settings.tile_size + 10, self.y_value+4)
		self.screen.blit(self.msg_image, self.msg_image_rect)


def draw_icons(grass_icon, water_icon,lava_icon):
	grass_icon.draw_icon()
	water_icon.draw_icon()
	lava_icon.draw_icon()

def run_game():
	pygame.init()
	clock = pygame.time.Clock()
	game_settings = Settings()
	screen = pygame.display.set_mode((game_settings.window_width, game_settings.window_height))
	pygame.display.set_caption("Minecraft")
	screen.fill(game_settings.window_color)
	tile_map = create_tile_map(game_settings)
	hero = Player(screen, game_settings)
	inventory = Inventory(hero, game_settings)
	inventory_button = Button(game_settings,screen, "Inventory:")
	
	grass_icon = Icon(game_settings,screen,3,'GRASS', inventory)
	water_icon = Icon(game_settings,screen,7,'WATER', inventory)
	lava_icon = Icon(game_settings,screen, 11, 'LAVA', inventory)
	selected_icon = ''
	enemy = Enemy(screen, game_settings, tile_map)
	four_tiles = {}
	while True:
		
		screen.fill(game_settings.window_color)
		draw_tile_map(tile_map,game_settings,screen)
		for event in pygame.event.get():
			check_exit_action(event, game_settings)
			hero.move(event,game_settings, inventory_button)
			if event.type == pygame.MOUSEBUTTONDOWN:
				selected_icon = check_mouse_action(event, lava_icon, water_icon, grass_icon)
			place_selected_tile(selected_icon, inventory, event, tile_map, hero)
			decrement_inventory(selected_icon, event, inventory)
		inventory.add_to_inventory(hero,event,tile_map)
		hero.upate_image()
		
		hero.blit(game_settings)
		enemy.move(hero, game_settings)
		enemy.blit()
		inventory_button.draw_button(game_settings, screen)
		draw_icons(grass_icon, water_icon,lava_icon)
		place_selected_tile(selected_icon, inventory, event, tile_map, hero)
		check_game_over(hero, enemy, clock)
		check_four_squares(tile_map, game_settings, four_tiles)
		fill_in_four_tiles(four_tiles, tile_map)
		clock.tick(game_settings.fps)
		pygame.display.flip()
		
run_game()


