import pygame
import sys
import time
import random
from pygame.locals import QUIT

# setup

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800

CELL_SIZE = 10

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()

pygame.display.set_caption('Snake')

# classes

class Snake:

	def __init__(self, start_pos_x, start_pos_y):
		self.parts = [(start_pos_x, start_pos_y)]
		self.move_direction = (0, 0)

	def move(self):
		previous_part = self.parts[0]

		# move the head
		self.parts[0] = (self.parts[0][0] + self.move_direction[0], self.parts[0][1] + self.move_direction[1])

		# teleport to the other side if hit boundaries
		if (self.parts[0][0] < 0):
			self.parts[0] = (SCREEN_WIDTH - CELL_SIZE, self.parts[0][1])
		elif (self.parts[0][0] >= SCREEN_WIDTH):
			self.parts[0] = (0, self.parts[0][1])
		elif (self.parts[0][1] < 0):
			self.parts[0] = (self.parts[0][0], SCREEN_HEIGHT - CELL_SIZE)
		elif (self.parts[0][1] >= SCREEN_HEIGHT):
			self.parts[0] = (self.parts[0][0], 0)

		# move the tail
		for i in range(1, len(self.parts)):
			temp = self.parts[i]
			self.parts[i] = previous_part
			previous_part = temp

	def draw(self):
		for pos_x, pos_y in self.parts:
			pygame.draw.rect(surface, (0, 255, 0), pygame.Rect(pos_x, pos_y, CELL_SIZE, CELL_SIZE))

	def change_dir(self, pos_x, pos_y):
		if ((pos_x != 0 and self.move_direction[0] == 0) or (pos_y != 0 and self.move_direction[1] == 0)):
			self.move_direction = (pos_x, pos_y)

	def add_part(self):
		self.parts.append((self.parts[0][0] + self.move_direction[0], self.parts[0][1] + self.move_direction[1]))

	def check_for_apple(self, apple):
		if self.parts[0][0] == apple.x and self.parts[0][1] == apple.y:
			self.add_part()
			return True

		return False

	def bite_check(self):
		head = self.parts[0]

		for i in range(1, len(self.parts)):
			if head == self.parts[i]:
				self.parts = self.parts[0:i]
				break

snake = Snake(80, 60)

class Apple:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def draw(self):
		pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(self.x, self.y, CELL_SIZE, CELL_SIZE))

	@staticmethod
	def spawn_apple():
		x = random.randrange(0, SCREEN_WIDTH - CELL_SIZE, CELL_SIZE)
		y = random.randrange(0, SCREEN_HEIGHT - CELL_SIZE, CELL_SIZE)
		apple = Apple(x, y)
		return apple

# state

move_direction = [0, 0]
apple = Apple.spawn_apple()

# functions

def quit():
	pygame.quit()
	sys.exit()

def input():
	events = pygame.event.get()

	for event in events:
		# keyboard events
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				move_direction[0] = -CELL_SIZE
				move_direction[1] = 0
			elif event.key == pygame.K_RIGHT:
				move_direction[0] = CELL_SIZE
				move_direction[1] = 0
			elif event.key == pygame.K_UP:
				move_direction[1] = -CELL_SIZE
				move_direction[0] = 0
			elif event.key == pygame.K_DOWN:
				move_direction[1] = CELL_SIZE
				move_direction[0] = 0

		if event.type == QUIT:
			quit()

# game loop

game_on = True
while game_on:
	screen.blit(surface, (0, 0))
	surface.fill((0, 0, 0))

	input()

	apple.draw()

	snake.change_dir(move_direction[0], move_direction[1])
	snake.move()

	if snake.check_for_apple(apple):
		apple = Apple.spawn_apple()
		apple.draw()

	snake.bite_check()
	snake.draw()

	pygame.display.update()
	clock.tick(30)
