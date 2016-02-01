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
from Dead import *
import PyGameFuncs

from sys import argv ###################
#######################################################################

subject_num = ''
if len(sys.argv)>1: #ie if a subject number was input
	subject_num = str(sys.argv[1])
else:
	print("PLEASE ENTER THE PARTICIPANT NUMBER. (Open program by typing eg 'python Output.py 001'")

camera = Camera()
user = MazeMove(camera)

maze = Maze()
hallway_type = maze.current_type()
inventory = Inventory(maze)
output2d = Output2d(camera, inventory, maze)
writefile = WriteFile(maze, subject_num)
time = Time(maze)
dead = Dead(output2d, time, writefile)
glutInit()
was_focused = False

fps = 1000 #added this to try sotp flickering (frames per sec) -didn't work :(

##

def display():
	output2d.draw_images()
	output2d.draw_inv_text()
	
	hallway_type = maze.current_type()

	GLComponents.hallway(hallway_type, True, maze.position.colours)

	pygame.display.flip()	#Refresh screen
	#pygame.time.Clock().tick(fps) ############
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)	#Clear buffer

def display_selected(direction_string):
	output2d.draw_images()
	output2d.draw_inv_text()	
	output2d.draw_selected_dirn(direction_string) 
	pygame.display.flip() 
	#pygame.time.Clock().tick(fps) ##########
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	
def refresh_focus():	#refresh the screen when someone focuses on it (needed on windows)
	global was_focused
	if pygame.key.get_focused() and not was_focused:	#Update when screen selected
		display()
		was_focused = True
	was_focused = pygame.key.get_focused()
		
def display_straight(delay, winning_spot):
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	
	if winning_spot and maze.give_prize(inventory):	#Note the use of short circuit operators here. Be careful
		output2d.winning_message()
		#GLComponents.prize_picture(maze.position.prize[0]) #can add this for images I think??????not quite sure what it does, only seems to work sometimes (maybe its selecting nones sometimes)
	
	#GLComponents.prize_picture('food')
	output2d.draw_inv_text()  
	GLComponents.hallway(Hallways.STRAIGHT, True, MazeComponent.generate_colours(Hallways.STRAIGHT)) 

	pygame.display.flip() 
	time.mri_delay(delay)		#Show first hallway		
	#pygame.time.Clock().tick(fps) #####################	

def three_hallways_step():	#When an option is selected, show hallway, prize, hallway
	display_straight(time.get_wait_time(), False)
	time.reset()
	display_straight(PRIZE_DELAY, True)

	dead_inventory = inventory.is_dead()	#Did an inventory item drop below minimum?
	if True in dead_inventory:	#Might have died here
		dead.death(dead_inventory)
		#if i want to make multiple lives, after here, reinitialize hte maze stuff from above that i want to reset, and return false, break out of this function, then make sure the functions caling it (step?) breaks when it recieves false from this guy (increment # lives either here or in the dead.py stuff)
	time.reset()
	display_straight(time.get_wait_time(), False)
	time.reset()
	
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	hallway_type = maze.current_type()
				
#Whenever the user steps from a choice room
def step(direction, key_pressed, direction_string):
	
	if MRI_ON:
		while not (time.mri_increment() and time.num_chars >= TIME_DECIDE/MRI_TIME):
			PyGameFuncs.event_loop()
			refresh_focus() #so this displays screen for MIN of time decide, and then moves on at hte next 5 keypress??
	else:
		time.mri_delay(TIME_DECIDE) #############Displays for n secs after decision???
		
	time.reset()	#Start from 0
	
	display_selected(direction_string)##maybe move this???
	time.mri_delay(CHOICE_DELAY)#?
	#time.reset()#?
		
	writefile.add_output_buffer_prelim(subject_num)	#Write to file with preliminary info. 
	current_inventory = inventory.inventory
	
	maze.step(direction)	#Move
	maze.increment_step_count()
	#display()	#Just in case, refresh
		
	decrement_amounts = inventory.decrement()
	
	PyGameFuncs.wait_key_up(key_pressed)	#Present message about prize, wait for key release 
	#########not sure why this is here. ie about timing and stuff (go test if it works ok later)
	writefile.add_output_buffer_postlim(direction_string, current_inventory, decrement_amounts)	#Add more to output
	writefile.flush_output(subject_num)	#Output to file
	
		#Display 
	#pygame.display.flip()
	
	three_hallways_step()
	#print 'depth ' + str(maze.position.depth)
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
		#pygame.time.Clock().tick(fps) #arg is frames per sec. not the most accurate timing??? #may not be good
		
#############
display()
#pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN|pygame.HWSURFACE|pygame.OPENGL| pygame.DOUBLEBUF) # pygame.FULLSCREEN| #not sure the doublebuf worked (I think it did...) but fullscreen is fun.

run()

