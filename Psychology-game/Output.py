'''Controls the screen and user input. The main loop is located here.'''


import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from Output2d import *

import random #To choose which path

from User import *
from Globals import *

import GLComponents

from Camera import *
from math import sin, cos

from Maze import *
from WriteFile import *
#######################################################################

camera = Camera(700, 700)
user = MazeMove(camera)

maze = Maze(Hallways.TRIFURC)
hallway_type = maze.current_type()
inventory = Inventory()
output2d = Output2d(camera, inventory, maze)
writefile = WriteFile(inventory, maze)
glutInit()

#Wait for key to be lifted to continue
def wait_key_up(key):
	
	if maze.give_prize(inventory):
			output2d.winning_message()
	
	GLComponents.hallway(maze.current_type(), True, maze.position.colours)							
	pygame.display.flip()
	
	
	while pygame.key.get_pressed()[key]:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:	#Quit if you leave the window
				pygame.quit()
				quit()
				
#Whenever the user steps
def step(direction, key_pressed):
	writefile.add_output_buffer_prelim()	#Write to file. 
	maze.step(direction)	#Move
				
	wait_key_up(key_pressed)	#Present message about prize, wait for key release
	writefile.add_output_buffer_postlim()	#Add more to output
	writefile.flush_output()	#Output to file
	
#######################################################################
def run():	
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:	#Quit if you leave the window
				pygame.quit()
				quit()				
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)	#Clear buffer
				
		output2d.draw_images()
		output2d.draw_inv_text()
				
		
		if pygame.key.get_pressed()[pygame.K_UP]:
			if hallway_type not in [Hallways.LEFT, Hallways.RIGHT, Hallways.BIFURC]:
				step(Directions.FORWARDS, pygame.K_UP)

		elif pygame.key.get_pressed()[pygame.K_DOWN] and maze.position.adjacent[Directions.BACKWARDS] != None:
			step(Directions.BACKWARDS,pygame.K_DOWN)
			
		elif pygame.key.get_pressed()[pygame.K_LEFT]:
			if hallway_type not in [Hallways.STRAIGHT, Hallways.RIGHT, Hallways.RIGHT_BIFURC]:
				step(Directions.LEFT, pygame.K_LEFT)
				
		elif pygame.key.get_pressed()[pygame.K_RIGHT]:
			if hallway_type not in [Hallways.STRAIGHT, Hallways.LEFT, Hallways.LEFT_BIFURC]:
				step(Directions.RIGHT, pygame.K_RIGHT)
		
		hallway_type = maze.current_type()
		
		GLComponents.hallway(hallway_type, True, maze.position.colours)
			
		pygame.display.flip()	#Refresh screen
		pygame.time.wait(25)
#############
run()
