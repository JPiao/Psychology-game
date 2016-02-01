'''This file stores information about the user's position in the maze. 
The user is able to turn different directions, have certain resources, 
etc.'''

import pygame

from math import radians, sin, floor

import GLComponents
import ReadFile

class MazeMove:
	#Maze
	#Position
	camera = None	#Instance for Camera
	transl_amount = 0	#How much to translate each step
	turn_amount = 0	#How many degrees to rotate per step. Make this a factor of 90
	distance_from_wall = 0 #How many units do you stop before getting to a door. Should be in the form 1/n
	
	def __init__(self, camera, transl_amount = 0.05, turn_amount = 2, distance_from_wall = 3):
		self.camera = camera
		self.turn_amount = turn_amount
		self.transl_amount = transl_amount
		self.distance_from_wall = distance_from_wall
	
	
	def turn_left(self):
		if self.camera.coord[2] < 4:	#Advance to back
			self.camera.advance(self.transl_amount)
		elif self.camera.angle == 0 or self.camera.angle > 270:	#Turn left
			pygame.time.wait(40)
			self.camera.turnHoriz(-self.turn_amount)
			#Make sure the person only moves forward exactly one unit
			#sum of cos(x) for normalization
			normalizer = 1/2.0 + sin((floor(90/self.turn_amount) + .5) * self.turn_amount * 3.14159/180)/(2*sin(self.turn_amount * 3.14159/180/2))
			
			self.camera.advance(2/normalizer)
			
		elif abs(self.camera.coord[0]) < 6 - self.distance_from_wall:	#Go to door
			self.camera.advance(self.transl_amount)
		else:	#finished
			#pygame.time.wait(500)	#Wait at door
			#self.camera.reset()		#Reset location
			return True
		return False
			
		
	def turn_right(self):
		if self.camera.coord[2] < 4:	#Advance to back
			self.camera.advance(self.transl_amount)
		elif self.camera.angle < 90:	#Turn right
			pygame.time.wait(40)
			self.camera.turnHoriz(self.turn_amount)
			
			#Make sure the person only moves forward exactly one unit
			#sum of cos(x) for normalization
			normalizer = 1/2.0 + sin((floor(90/self.turn_amount) + .5) * self.turn_amount * 3.14159/180)/(2*sin(self.turn_amount * 3.14159/180/2))
			
			self.camera.advance(2/normalizer)
		elif abs(self.camera.coord[0]) < 6 - self.distance_from_wall:	#Go to door
			self.camera.advance(self.transl_amount)
		else:	#finished
			return True
		return False

	def straight(self):
		if self.camera.coord[2] < 5 - self.distance_from_wall:
			self.camera.advance(self.transl_amount)
			return False
		return True

	'''Go straight with a trifurcation'''
	def far_straight(self):
		if self.camera.coord[2] < 9 - self.distance_from_wall:
			self.camera.advance(self.transl_amount)
			return False
		return True
		
	def reset(self):
		self.camera.reset()

#Keep track of inventory
class Inventory:
	def __init__(self, maze):
		self.maze = maze
		self.inventory = {}
		for inv_type in ReadFile.get_inventory_types():
			self.inventory[inv_type] = 0
	
	def decrement(self):
		decrement_vals = ReadFile.read_decrement()	#Read in how much to decrement by
		inv_types = ReadFile.get_inventory_types()
		
		decrement_amounts = [0, 0, 0]
		
		for x in range(len(decrement_vals)):
			if (self.maze.total_step_count ) % decrement_vals[x][0] == 0:	#Should dec?
				self.inventory[inv_types[x]] -= decrement_vals[x][1]
				decrement_amounts[x] = decrement_vals[x][1]
		return decrement_amounts
	
	'''Gives the prize. inv_type is a number, not a string'''
	def give_prize(self, inv_type, amount):	
		num = -1
		for x in range(len(ReadFile.get_inventory_types())):	#Get the inv num
			if ReadFile.get_inventory_types()[x] == inv_type:
				num = x
				break	
				
		cap = ReadFile.read_caps()[num]
		if cap == None:	#Unbounded cap
			self.inventory[inv_type] += amount
		else:	#Bounded cap
			difference = cap - self.inventory[inv_type]	#How much left can be added
			self.inventory[inv_type] += min(difference, amount)
