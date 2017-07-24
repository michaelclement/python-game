"""
Michael Clement Final Project
for interactive programming.

This is a game where you play as a little man
trying to avoid enemies and collect goals. 

"""
import pygame
import random
# This is for the explosion animations
import sys

# --- Global constants ---
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0) 
GREEN = (0,255,0)
BLUE = (70,70,255)
 
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700



# --- Functions
# This is for the explosion animations
def load_image(name):
	image = pygame.image.load(name)
	
	return image

# --- Classes

class Block(pygame.sprite.Sprite):
	"""
	This is the enemy class.
	"""
	def __init__(self, color, width, height):
		""" Constructor. Pass in the color of the block,
		and its x and y position. """
		# Call the parent class (Sprite) constructor
		super().__init__()
		
		# This is meant to work with the below code for changing
		# Which sprite image gets picked.
		iteration = 0
		frame = 0

		# list of sprites:
		ghost_spritesheet = ["ghost_spritesheet1.png", "ghost_spritesheet2.png","ghost_spritesheet3.png"]
 
		# This is meant to change the sprite image every 10 frames, but currently
		# all it does is allow the computer to pick a random sprite
		# when first drawing the object...
		if iteration%10 == 0: 
			frame = random.choice([0,1,2])
		self.image = pygame.image.load(ghost_spritesheet[frame]).convert()
		iteration += 1
		
		# Create an image of the enemy
		self.image.set_colorkey(BLACK)
 
		# Fetch the rectangle object that has the dimensions of the image
		self.rect = self.image.get_rect()
 
		# Instance variables that control the edges of where it bounces
		self.left_boundary = 0
		self.right_boundary = 0
		self.top_boundary = 0
		self.bottom_boundary = 0
 
		# Instance variables for current speed and direction
		self.change_x = 0
		self.change_y = 0
 
	def update(self):
		""" Called each frame to update the 
		position of the enemies. 
		"""
		self.rect.x += self.change_x
		self.rect.y += self.change_y
 
		if self.rect.right >= self.right_boundary or self.rect.left <= self.left_boundary:
			self.change_x *= -1
 
		if self.rect.bottom >= self.bottom_boundary or self.rect.top <= self.top_boundary:
			self.change_y *= -1

class Player(Block):
	
	""" This is the player class, deriving 
	from the enemy (block) class
	"""
	# -- Methods
	def __init__(self, x, y, color):
		"""Constructor function"""
		# Call the parent's constructor
		# The parameters within this dictate the size and color of main player
		super().__init__(RED, 15, 15)
 
		# Set image of the player
		self.image = pygame.image.load("human_sprite.png").convert()
		self.image.set_colorkey(BLACK) 
				
		# starting position of player:
		self.rect.x = 10
		self.rect.y = 560
 
		# Set speed vector
		self.change_x = 0
		self.change_y = 0
		
		# Set a reference to the image rect.
		self.rect = self.image.get_rect()

	def changespeed(self, x, y):
		""" Change the speed of the player"""
		self.change_x += x
		self.change_y += y
 
	def update(self):
		""" Find a new position for the player"""
		self.rect.x += self.change_x
		self.rect.y += self.change_y
		
		# Checks to see if player has hit a wall.
		if self.rect.x > SCREEN_WIDTH - 20:
			self.rect.x = SCREEN_WIDTH - 20
		if self.rect.x < 0:
			self.rect.x = 1
		if self.rect.y < 0:
			self.rect.y = 1
		if self.rect.y > SCREEN_HEIGHT - 45:
			self.rect.y = SCREEN_HEIGHT - 45 
	
	def calc_grav(self):
		if self.change_y == 0:
			self.change_y = 3
		else:
			self.change_y += 1
 
		# See if we are on the ground.
		if self.rect.y >= 620 - self.change_y >= 0:
			self.change_y = 0
			self.rect.y = 620
	
	def reset(self):
		# This resets the player when he comes into contact with an enemy
		self.rect.x = 1
		self.rect.y = SCREEN_HEIGHT - 10




class Explosion(pygame.sprite.Sprite):
	'''This class is for the explosions that are triggered by
	colliding with an enemy. It requires 7 images'''
	def __init__(self, x, y):
		super(Explosion, self).__init__()
		self.counter = 0
		self.images = []
		self.images.append(load_image('boom1.png'))
		self.images.append(load_image('boom2.png'))
		self.images.append(load_image('boom3.png'))
		self.images.append(load_image('boom4.png'))
		self.images.append(load_image('boom5.png'))
		self.images.append(load_image('boom6.png'))
		self.images.append(load_image('boom7.png'))

		# assuming both images are 64x64 pixels
		self.index = 0
		self.image = self.images[self.index]
		
		self.rect = pygame.Rect(x, y,64,64)

	def update(self):
		'''This method iterates through the elements inside self.images and 
		displays the next one each tick. to change the speed of the animation
		simply change the "if self.counter > x number" '''
		if self.counter > 2:
			self.counter = 0
			self.index += 1
		else:
			self.counter += 1
		
		if self.index >= len(self.images):
			self.index = 0
		self.image = self.images[self.index]






class Goal(pygame.sprite.Sprite):
	"""
	This is a new class similar to block, but 
	meant to be the collectibles.
	"""
	def __init__(self, color, width, height):
		""" Constructor. Pass in the color of the block,
		and its width and height. """
		# Call the parent class (Sprite) constructor
		super().__init__()
 
		# Create an image of the block, and fill it with a color.
		self.image = pygame.Surface([width, height])
		self.image.fill(color)
 
		# Fetch the rectangle object that has the dimensions of the image
		# Update the position of this object by setting the values of rect.x and rect.y
		self.rect = self.image.get_rect()
		self.rect.x = SCREEN_WIDTH - 30
		self.rect.y = SCREEN_HEIGHT - 45
		
class Health(pygame.sprite.Sprite):
	"""
	This is a new class similar to block, but 
	meant to be the collectibles. These give the player +2 lives.
	"""
	def __init__(self, color, width, height):
		# Call the parent class (Sprite) constructor
		super().__init__()
 
		self.image = pygame.Surface([width, height])
		self.image.fill(color)
 
		self.rect = self.image.get_rect()
		self.rect.x = SCREEN_WIDTH - 30
		self.rect.y = SCREEN_HEIGHT - 30

class Safe_Zone(pygame.sprite.Sprite):
	"""
	This class makes an area that is safe for the player to stand in. Any enemies that
	come into contact with it are removed. The safe zone is in the area where the player first
	spawns.
	"""
	def __init__(self, color, width, height):
		# Call the parent class (Sprite) constructor
		super().__init__()
		
		self.image = pygame.Surface([width, height])
		self.image.fill(color)
 
		self.rect = self.image.get_rect()
		self.rect.x = 0
		self.rect.y = 623

#---- Game Class

class Game(object):
	""" This class represents an instance of the game. to reset the game
	simply make a new instance of it. """
	def __init__(self):
		""" Constructor. Create all our attributes and initialize
		the game. """
		
		# Counters for various collisions 
		self.lives = 100
		self.score = 0
		self.level = 1
		
		#self.hit_location_x = 0
		#self.hit_location_y = 0
		
		self.game_over = False
 		
		# Sounds for when player hits certain items.
		self.death_sound = pygame.mixer.Sound("death_sound.ogg")
		self.health_hit_sound = pygame.mixer.Sound("health_hit_sound.ogg")
		self.goal_hit_sound = pygame.mixer.Sound("goal_hit_sound.ogg") 
		self.level_complete_sound = pygame.mixer.Sound("level_complete_sound.ogg")
		self.game_over_music = pygame.mixer.Sound("game_over_music.ogg")

		# ------ Create Sprite Lists
		
				
		# holds all the enemies
		self.block_list = pygame.sprite.Group()

		# This list handles when the player hits a goal
		self.goal_list = pygame.sprite.Group()
		
		# holds the health pickups
		self.health_list = pygame.sprite.Group()
		
		# holds the safe zone
		self.safety_list = pygame.sprite.Group()
		
		# This is a list of every sprite. All blocks and the player block as well.
		self.all_sprites_list = pygame.sprite.Group()
		

		for i in range(10):
			# This creates the initial wave of enemies on level 1
			self.block = Block(WHITE, 25, 15)
		 
			# Set a random location for the block
			self.block.rect.x = random.randrange(25, 870)
			self.block.rect.y = random.randrange(SCREEN_HEIGHT)
		 
			self.block.change_x = random.randrange(-3, 4)
			self.block.change_y = random.randrange(-3, 4)
			self.block.left_boundary = 0
			self.block.top_boundary = 0
			self.block.right_boundary = SCREEN_WIDTH
			self.block.bottom_boundary = SCREEN_HEIGHT
		 
			# Add the block to the list of objects
			self.block_list.add(self.block)
			self.all_sprites_list.add(self.block)

		# creates safe zones
		self.safe_zone = Safe_Zone(RED, 75, 80)
		self.safe_zone.image = pygame.image.load("dojo.png").convert()
		self.safe_zone.image.set_colorkey(BLACK)
		self.safe_zone.rect.x = 10
		self.safety_list.add(self.safe_zone)
		self.all_sprites_list.add(self.safe_zone)
	  
		# Creates the player
		self.player = Player(RED, 20, 15)
		self.player.calc_grav()
		self.player.reset()
		self.all_sprites_list.add(self.player)
		
		# creates goal
		self.goal = Goal(GREEN, 10, 50)
		self.goal_list.add(self.goal)
		self.all_sprites_list.add(self.goal)

				
	def process_events(self):
		""" Process all of the events. Return a "True" if we need
			to close the window. """
 
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return True
			if event.type == pygame.MOUSEBUTTONDOWN:
				if self.game_over:
					self.__init__()
			elif event.type == pygame.constants.USEREVENT:
					# This event is triggered when the song stops playing.
					pygame.mixer.music.load('background_music.ogg')
					pygame.mixer.music.play()
						
			# Set the speed based on the key pressed
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					self.player.changespeed(-10, 0)
				elif event.key == pygame.K_RIGHT:
					self.player.changespeed(10, 0)
				elif event.key == pygame.K_UP:
					self.player.changespeed(0, -15)
				elif event.key == pygame.K_DOWN:
					self.player.changespeed(0, 10)
	 
			# Reset speed when key goes up
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT:
					self.player.changespeed(10, 0)
				elif event.key == pygame.K_RIGHT:
					self.player.changespeed(-10, 0)
				elif event.key == pygame.K_UP:
					self.player.changespeed(0, 15)
				elif event.key == pygame.K_DOWN:
					self.player.changespeed(0, -10)	
 
		return False
 
	def run_logic(self):
		"""
		This method is run each time through the frame. It
		updates positions and checks for collisions.
		"""
		if not self.game_over:
			# Move all the sprites
			self.all_sprites_list.update()
 
			# See if the player block has collided with anything or if enemies have collided
			# with the safe zone.
			blocks_hit_list = pygame.sprite.spritecollide(self.player, self.block_list, True)
			goal_hit_list = pygame.sprite.spritecollide(self.player, self.goal_list, True)
			safe_zone_hit_list = pygame.sprite.spritecollide(self.safe_zone, self.block_list, True)
			health_hit_list = pygame.sprite.spritecollide(self.player,self.health_list, True)
 
			# Check the list of collisions.
			for block in blocks_hit_list:
				self.lives -= 5
				self.death_sound.play()
				
				# This is the group of sprites for explosion effects
				# This creates the explosion at the location where the player
				# collided with the ghost.
				self.hit_location_x = self.player.rect.x
				self.hit_location_y = self.player.rect.y		
				self.explosion = Explosion(self.hit_location_x,self.hit_location_y)
				self.my_group = pygame.sprite.Group(self.explosion)
				
				
				print("The location of the explosion is:",self.player.rect.x,self.player.rect.y)
				self.player.reset()
				
			for goal in goal_hit_list:
				self.score += 1
				self.goal_hit_sound.play()
			# When the player collects a health power up
			# The are returned to 20 lives
			for health in health_hit_list:
				if self.lives <= 100:
					self.lives += (100 - self.lives)
				self.health_hit_sound.play()
			for block in safe_zone_hit_list:
				'''
				This creates a new enemy every time one is destroyed by
				the safe zone. This prevents the player from just waiting
				until the level beats itself.
				'''
				self.block = Block(WHITE, 25, 15)
				# Set a random location for the block
				self.block.rect.x = random.randrange(25, 870)
				self.block.rect.y = random.randrange(SCREEN_HEIGHT)
			 
				self.block.change_x = random.randrange(-3, 4)
				self.block.change_y = random.randrange(-3, 4)
				self.block.left_boundary = 0
				self.block.top_boundary = 0
				self.block.right_boundary = SCREEN_WIDTH
				self.block.bottom_boundary = SCREEN_HEIGHT
			 
				# Add the block to the list of objects
				self.block_list.add(self.block)
				self.all_sprites_list.add(self.block)

			# Causes a game over if the player loses all their lives
			if self.lives <= 0:
				self.game_over_music.play()
				self.game_over = True

		# Check to see if all the blocks are gone. If they are, level advances.
		if len(self.goal_list) == 0:
			# Add one to the level
			self.level += 1
			self.level_complete_sound.play()
			self.player.reset()
			print(self.level)

			# Add more blocks. How many depends on the level.
			for i in range(10):
				# This represents a goal
				self.goal = Goal(GREEN, 10, 50)
				self.goal_list.add(self.goal)
				self.all_sprites_list.add(self.goal)
				
				# Set a random location for the block
				self.goal.rect.x = random.randrange(SCREEN_WIDTH)
				self.goal.rect.y = random.randrange(SCREEN_HEIGHT)
				 
				# Add the block to the list of objects
				self.goal_list.add(self.goal)
				self.all_sprites_list.add(self.goal)
			
			for i in range(self.level * 5):
				# This represents a goal
				self.block = Block(WHITE, 20, 20)
				self.block_list.add(self.block)
				self.all_sprites_list.add(self.block)
	 
				# Set a random location for the block
				self.block.rect.x = random.randrange(SCREEN_WIDTH)
				self.block.rect.y = random.randrange(SCREEN_HEIGHT)
				# block movement
				self.block.change_x = random.randrange(-5, 7)
				self.block.change_y = random.randrange(-5, 7)
				self.block.left_boundary = 0
				self.block.top_boundary = 0
				self.block.right_boundary = SCREEN_WIDTH
				self.block.bottom_boundary = SCREEN_HEIGHT

				# Add the block to the list of objects
				self.block_list.add(self.goal)
				self.all_sprites_list.add(self.goal)
			
			for i in range(2):
				# This represents a goal
				self.health = Health(BLUE, 10, 50)
				self.health_list.add(self.health)
				self.all_sprites_list.add(self.health)
	 
				# Set a random location for the block
				self.health.rect.x = random.randrange(SCREEN_WIDTH)
				self.health.rect.y = random.randrange(SCREEN_HEIGHT)
				 
				# Add the block to the list of objects
				self.health_list.add(self.health)
				self.all_sprites_list.add(self.health)

	def display_frame(self, screen):
		""" Display everything to the screen for the game. """
		screen.fill(BLACK)
		
		if self.game_over:
			# background image for game over screen
			background_image = pygame.image.load("background.png").convert()
			background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH,SCREEN_HEIGHT))
			screen.blit(background_image, [0, 0])
			# game over text.
			font = pygame.font.SysFont("serif", 25)
			text = font.render("Game over. You scored: " + str(self.score), True, WHITE)
			center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
			center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2)
			screen.blit(text, [center_x, center_y])
			# Click to restart text
			font = pygame.font.SysFont("serif", 45)
			text = font.render("Click to restart.", True, WHITE)
			center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
			center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2)
			screen.blit(text, [center_x, center_y + 55])
 
		if not self.game_over:
			'''
			# background image for main game (commented out because it makes the game too laggy)
			background_image = pygame.image.load("background.png").convert()
			background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH,SCREEN_HEIGHT))
			screen.blit(background_image, [0, 0])
			'''
			# Draws all sprites
			self.all_sprites_list.draw(screen)
			
			# This draws an explosion when the player has hit an enemy
			if self.lives < 100:
				self.explosion.update()
				self.my_group.draw(screen)
			
			# Blits lives count to screen	
			font = pygame.font.SysFont('Calibri', 40, True, False)
			text = font.render("Health: %" + str(self.lives), True, BLUE)	 
			screen.blit(text, [10, 10])
			
			# Blits level count to screen	
			font = pygame.font.SysFont('Calibri', 40, True, False)
			text = font.render("Level: " + str(self.level), True, WHITE)	 
			screen.blit(text, [230, 10])
			
			# Blits score to screen	
			font = pygame.font.SysFont('Calibri', 40, True, False)
			text = font.render("Score: " + str(self.score), True, GREEN)	 
			screen.blit(text, [380, 10])
			
			# Blits controls to screen	
			font = pygame.font.SysFont('Calibri', 40, True, False)
			text = font.render("Use arrow keys to move player", True, WHITE)	 
			screen.blit(text, [530, 10])
		
		pygame.display.flip()
 
def main():
	""" Main program function. """
	# Initialize Pygame and set up the window
	pygame.init()
 
	size = [SCREEN_WIDTH, SCREEN_HEIGHT]
	screen = pygame.display.set_mode(size)
 
	pygame.display.set_caption("Game")
 
	done = False
	clock = pygame.time.Clock()
 
	# Create an instance of the Game class
	game = Game()
	
	# Background Music
	pygame.mixer.music.load('background_music.ogg')
	pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
	pygame.mixer.music.play()
	
	# counter for instruction page.	 
	display_instructions = True
	instruction_page = 1
	 
	# -------- Instruction Page Loop -----------
	while not done and display_instructions:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
			if event.type == pygame.MOUSEBUTTONDOWN:
				instruction_page += 1
				if instruction_page == 2:
					display_instructions = False
	 
		# Set the screen background
		screen.fill(BLACK)
	 
		if instruction_page == 1:
			# Makes a page that lists how to play the game	
			
			background_image = pygame.image.load("background.png").convert()
			background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH,SCREEN_HEIGHT))
			screen.blit(background_image, [0, 0]) 
			
			# This is a font for the instruction page
			font = pygame.font.Font(None, 42)
			text = font.render("Instructions", True, WHITE)
			screen.blit(text, [10, 10])
			
			font = pygame.font.Font(None, 25)
			text = font.render("Use the keyboard's arrow keys to move your player.", True, WHITE)
			screen.blit(text, [10, 70])
			
			# There is a space in the text of this line because it makes room for the word "green"
			text = font.render("Avoid ghosts and collect the           blocks to advance.", True, WHITE)
			screen.blit(text, [10, 110])
			text = font.render("green", True, GREEN)
			screen.blit(text, [245, 110])
			
			# There is a space in the text of this line because it makes room for the word "blue"
			text = font.render("Grab         blocks to gain lives!", True, WHITE)
			screen.blit(text, [10, 150])
			text = font.render("blue", True, BLUE)
			screen.blit(text, [55, 150])
			
			# This tells the player to click in order to start the game.
			pygame.draw.rect(screen, RED, [445, 280, 300, 70],4)
			font = pygame.font.Font(None, 50)
			text = font.render("Click to play!", True, RED)
			screen.blit(text, [490, 300])
			
		# Limit to 60 frames per second
		clock.tick(60)
	 
		# Go ahead and update the screen with what we've drawn.
		pygame.display.flip()
	
	#---- Main game loop
	while not done:

		# Process events (keystrokes, mouse clicks, etc)
		done = game.process_events()
 
		# Update object positions, check for collisions
		game.run_logic()

		# Draw the current frame
		game.display_frame(screen)
						 
		# Pause for the next frame
		clock.tick(60)
 
	# Close window and exit
	pygame.quit()
 
# Call the main function, start up the game
if __name__ == "__main__":
	main()