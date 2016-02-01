import GLComponents
from OpenGL.GL import *
from OpenGL.GLUT import *
import pygame

from Globals import *

import ReadFile

'''This file handles outputting 2d things, e.g. the inventory box and
	the cue images. These functions will be called in Output.py'''

class Output2d:
	#Give stuff for later
	def __init__(self, camera, inventory, maze):	#Just save the instances for later
		self.camera = camera
		self.inventory = inventory
		self.maze = maze
		
	#What is the width (px) of a string with a certain font?
	def str_width(self, string, font):
		return sum([glutBitmapWidth(font, ord(x)) for x in string])
		
	
	#Write the inventory stuff
	def draw_inv_text(self):	#Box around the text here
		PERCENT_UP = 0.95	#How far up is the text?
		FONT = GLUT_BITMAP_9_BY_15
		text_top = PERCENT_UP * self.camera.display[1] #Text starts from here
		
		GLComponents.glEnable2D()
		max_length = 0
		for item_num in range(len(self.inventory.inventory)):
			key = self.inventory.inventory.keys()[item_num]
			message = key + ': ' + str(self.inventory.inventory[key])
			
			width = self.str_width(message, FONT)
			
			if width > max_length:
				max_length = width
			GLComponents.write_str(message, 0, text_top - item_num * 15, FONT)
		
		GLComponents.draw_rect(0, max_length, text_top + 15, text_top - len(self.inventory.inventory) * 15)
		
		GLComponents.glDisable2D()

	#Show the inventory pictures
	def draw_images(self):
		width = self.camera.display[0]
		if self.maze.position.is_choice_room:
			inv_types = self.maze.position.prize_order
			if inv_types[0] != None:
				GLComponents.inventory_img(((0, 0), (0, 100), (100, 100), (100, 0)), inv_types[0] + IMAGE_EXT)
			if inv_types[1] != None:
				GLComponents.inventory_img(((width/2 - 50, 0), (width/2 - 50, 100), (width/2 + 50, 100), (width/2 + 50, 0)), inv_types[1] + IMAGE_EXT)
			if inv_types[2] != None:
				GLComponents.inventory_img(((width - 100, 0), (width - 100, 100), (width, 100), (width, 0)), inv_types[2] + IMAGE_EXT)

	#Display message when the user wins. 
	def winning_message(self):
		glDisable(GL_DEPTH_TEST)
		FONT = GLUT_BITMAP_HELVETICA_18
		WAIT = 2000 #How long is the message showing? In ms.
		
		message = 'You just got ' + str(self.maze.position.prize[1]) + ' ' + self.maze.position.prize[0] + '!'
		width = self.str_width(message, FONT)	#For centering
		
		GLComponents.glEnable2D()
		
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		
		#Centered text
		GLComponents.write_str(message, self.camera.display[0]/2 - width/2, self.camera.display[1]/2, FONT)
		
		#GLComponents.draw_rect(0, self.camera.display[0], 0, self.camera.display[1])
		GLComponents.glDisable2D()
		
		pygame.display.flip()
		pygame.time.wait(WAIT)
		
		glEnable(GL_DEPTH_TEST)
		
	
