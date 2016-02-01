import pygame
from Globals import *
import ReadFile
import random
import PyGameFuncs

class Time:
	def __init__(self, maze):
		self.time = pygame.time.get_ticks()
		self.maze = maze
		
		self.possible_times = ReadFile.read_times()
		self.next_straight_time = self.get_wait_time()
		
		self.num_chars = 0	#Number of times MRI outputs
	
	#Return how long to wait in the hall
	def get_wait_time(self):
		return int(self.possible_times[random.randint(0, len(self.possible_times) - 1)])

	def reset(self):
		self.time = pygame.time.get_ticks()
		self.num_chars = 0
	
	#increment numb_chars as needed
	def mri_increment(self):
		if pygame.key.get_pressed()[MRI_CHAR]:
			self.num_chars += 1
			PyGameFuncs.wait_key_up(MRI_CHAR)
			return True
		return False

	def mri_delay(self, time):
		while self.num_chars < time/MRI_TIME:
			PyGameFuncs.event_loop()
			self.mri_increment()
