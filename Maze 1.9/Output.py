'''Controls the screen and user input. The main loop is located here.'''

'''Make sure program works as possible. And CSV.'''
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
from MazeComponent import *
from WriteFile import *
from Time import *
import PyGameFuncs
#######################################################################

camera = Camera()
user = MazeMove(camera)

maze = Maze()
hallway_type = maze.current_type()
inventory = Inventory(maze)
output2d = Output2d(camera, inventory, maze)
writefile = WriteFile(maze)
time = Time(maze)
glutInit()
was_focused = False

def display():
	output2d.draw_images()
	output2d.draw_inv_text()
	
	hallway_type = maze.current_type()

	GLComponents.hallway(hallway_type, True, maze.position.colours)
	pygame.display.flip()	#Refresh screen
		
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)	#Clear buffer
	
def refresh_focus():	#refresh the screen when someone focuses on it
	global was_focused
	if pygame.key.get_focused() and not was_focused:	#Update when screen selected
		display()
		was_focused = True
	was_focused = pygame.key.get_focused()
		
def display_straight(delay, winning_spot):
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	
	GLComponents.hallway(Hallways.STRAIGHT, True, MazeComponent.generate_colours(Hallways.STRAIGHT))

	if winning_spot and maze.give_prize(inventory):	#Note the use of short circuit operators here. Be careful
		output2d.winning_message()
		#GLComponents.prize_picture(maze.position.prize[0])
	
	#GLComponents.prize_picture('food')
	output2d.draw_inv_text()
	pygame.display.flip()
	time.mri_delay(delay)		#Show first hallway		
		
def three_hallways_step():	#When an option is selected, show hallway, prize, hallway
	display_straight(time.get_wait_time(), False)
	time.reset()
	display_straight(PRIZE_DELAY, True)
	time.reset()
	display_straight(time.get_wait_time(), False)
	time.reset()
	
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	hallway_type = maze.current_type()
				
#Whenever the user steps from a choice room
def step(direction, key_pressed, direction_string):
	while not (time.mri_increment() and time.num_chars >= TIME_DECIDE/MRI_TIME):
		PyGameFuncs.event_loop()
		refresh_focus()
	time.reset()	#Start from 0
			
	writefile.add_output_buffer_prelim()	#Write to file with preliminary info. 
	current_inventory = inventory.inventory
	
	maze.step(direction)	#Move
	maze.increment_step_count()
		
	decrement_amounts = inventory.decrement()
	
	output2d.draw_selected()
	time.mri_delay(CHOICE_DELAY)
	time.reset()
	
	PyGameFuncs.wait_key_up(key_pressed)	#Present message about prize, wait for key release
	writefile.add_output_buffer_postlim(direction_string, current_inventory, decrement_amounts)	#Add more to output
	writefile.flush_output()	#Output to file
		#Display 
	#pygame.display.flip()
	
	three_hallways_step()
	print 'depth ' + str(maze.position.depth)
	display()
	
#######################################################################
def run():	
	while True:
		PyGameFuncs.event_loop()
		
		time.mri_increment()
				
		if pygame.key.get_pressed()[pygame.K_UP]:
			if hallway_type not in [Hallways.LEFT, Hallways.RIGHT, Hallways.BIFURC]:
				step(Directions.FORWARDS, pygame.K_UP, "centre")

		elif BACKWARDS_MOVE and pygame.key.get_pressed()[pygame.K_DOWN] and maze.position.adjacent[Directions.BACKWARDS] != None:
			step(Directions.BACKWARDS, pygame.K_DOWN, "back")
			
		elif pygame.key.get_pressed()[pygame.K_LEFT]:
			if hallway_type not in [Hallways.STRAIGHT, Hallways.RIGHT, Hallways.RIGHT_BIFURC]:
				step(Directions.LEFT, pygame.K_LEFT, "left")
				
		elif pygame.key.get_pressed()[pygame.K_RIGHT]:
			if hallway_type not in [Hallways.STRAIGHT, Hallways.LEFT, Hallways.LEFT_BIFURC]:
				step(Directions.RIGHT, pygame.K_RIGHT, "right")
				
		refresh_focus()
		
		hallway_type = maze.current_type()
#############
display()
run()
