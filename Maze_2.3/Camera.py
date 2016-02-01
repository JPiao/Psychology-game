'''FOR 3d. This class is used to keep track of the "location" of the camera. 
Essentially, it simply keeps track of all the rotational and
translational movement of the camera. This gives the ability to work 
relative to the origin of the maze game.'''


import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from Globals import *

import math

class Camera:
	coord = [0, 0, 0]
	angle = 0 #along the horizontal. Positive is to the right
	
	def __init__(self):
		#Start pygame
		pygame.init()
		
		pygame.display.set_icon(pygame.image.load(ICON_FILE))
		self.screen = pygame.display.set_mode(SCREEN_SIZE, DOUBLEBUF|OPENGL)
		pygame.display.set_caption(TITLE)
		
		gluPerspective(45, (SCREEN_SIZE[0]/SCREEN_SIZE[1]), .2, 50.0)	#Set up GL
		#camera.advance(-10)	
		glEnable(GL_DEPTH_TEST)	#Solid walls 
	
	#Translate the current coordinates
	def add(self, vector):
		for x in range(3):
			self.coord[x] += vector[x]
	
	#Move the camera forward
	def advance(self, amount):
		glTranslatef(-amount * math.sin(math.radians(self.angle)), 0, amount * math.cos(math.radians(self.angle)))
		self.coord[0] += -amount * math.sin(math.radians(self.angle))
		#self.coord[1] += y
		self.coord[2] += amount * math.cos(math.radians(self.angle))
		
	#Turn along the y-z plane. Angle in degrees.
	def turnHoriz(self, angle):
		glTranslatef(-self.coord[0], -self.coord[1], -self.coord[2])
		glRotatef(angle, 0, 1, 0)
		
		self.angle += angle
		self.angle = self.angle % 360 #Keep this 0 <= x < 360
				
		glTranslatef(self.coord[0], self.coord[1], self.coord[2])	
	
	#Start fresh from the origin, facing forwards
	def reset(self):
		glTranslatef(-self.coord[0], -self.coord[1], -self.coord[2])
		glRotatef(-self.angle, 0, 1, 0)
		
		self.coord = [0, 0, 0]
		self.angle = 0

	
