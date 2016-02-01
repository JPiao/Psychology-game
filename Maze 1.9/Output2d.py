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
		
	
	#Write the inventory stuff. Also loading bars
	def draw_inv_text(self):	#Box around the text here
		PERCENT_UP = 0.95	#How far up is the text?
		FONT = GLUT_BITMAP_9_BY_15
		LOADING_WIDTH = 40
		LOADING_HEIGHT = 10
		TEXT_LOADINGBAR_GAP = 10
		
		text_top = PERCENT_UP * SCREEN_SIZE[1] #Text starts from here
		
		GLComponents.glEnable2D()
		max_length = 0
		for item_num in range(len(self.inventory.inventory)):	#Longest sentence
			key = self.inventory.inventory.keys()[item_num]
			
			cap = ReadFile.read_caps()[item_num]
			if cap:
				message = "{0}: {1:.2f}%".format(key, self.inventory.inventory[key]/cap * 100.0)
			else:
				message = "{0}: {1:.2f}".format(key, self.inventory.inventory[key])
			
			width = self.str_width(message, FONT)
			
			if width > max_length:
				max_length = width
			GLComponents.write_str(message, 0, text_top - item_num * 15, FONT)
			if cap:	#Only capped values get loading bars
				GLComponents.loading_bar(max_length + TEXT_LOADINGBAR_GAP, text_top - 15 * item_num, 
					self.inventory.inventory[key]/cap * 100, LOADING_WIDTH, LOADING_HEIGHT)
		
		GLComponents.draw_rect(0, max_length + LOADING_WIDTH + TEXT_LOADINGBAR_GAP + 2, 
			text_top + 15, text_top - len(self.inventory.inventory) * 15)
		
		GLComponents.glDisable2D()

	#Show the inventory pictures
	def draw_images(self):
		width = SCREEN_SIZE[1]
		if self.maze.position.prize_order != [None, None, None]:
			inv_types = [x[2] if x else x for x in self.maze.position.prize_infos]
			if inv_types[0] != None:
				GLComponents.image_2d(((0, 0), (0, 100), (100, 100), (100, 0)), inv_types[0])
			if inv_types[1] != None:
				GLComponents.image_2d(((width/2 - 50, 0), (width/2 - 50, 100), (width/2 + 50, 100), (width/2 + 50, 0)), inv_types[1])
			if inv_types[2] != None:
				GLComponents.image_2d(((width - 100, 0), (width - 100, 100), (width, 100), (width, 0)), inv_types[2])
				
	#For showing the user information on a black background
	#A possible padding is allowed. Here it is given as a 1/100th of a percent
	def draw_centred(self, message, side_padding = 1, up_padding = 1):
		GLComponents.glEnable2D()
		if up_padding == 1 and side_padding == 1:	#Might as well clear all
			glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
			glDisable(GL_DEPTH_TEST)
		FONT = GLUT_BITMAP_HELVETICA_18
		
		width = self.str_width(message, FONT)	#For centering

		#Centered text
		GLComponents.write_str(message, SCREEN_SIZE[0]/2 - width/2, SCREEN_SIZE[1]/2, FONT)
		
		if up_padding != 1 or side_padding != 1:
			GLComponents.draw_rect(SCREEN_SIZE[0]/2 * (1 - side_padding), SCREEN_SIZE[0]/2 * (1 + side_padding), 
				SCREEN_SIZE[1]/2 * (1 - up_padding), SCREEN_SIZE[1]/2 * (1 + up_padding))
		
		self.draw_inv_text()

		GLComponents.glDisable2D()
		
		pygame.display.flip()
		
		glEnable(GL_DEPTH_TEST)
				
	#Show a picture and string of the object the user selected. 
	def draw_selected(self):
		message = 'You selected %s.' % self.maze.position.prize[0]
		self.draw_centred(message, )		
			
	#Display message when the user wins. 
	def winning_message(self):
		message = 'You just found ' + str(self.maze.position.prize[1]) + ' ' + self.maze.position.prize[0] + '!'
		self.draw_centred(message, 0.6, 0.3)		
		
	
