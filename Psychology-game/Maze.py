from MazeComponent import *
from Globals import *
import ReadFile
from random import random, randint
from User import *

class Maze:	
	#Pass in maze dimensions
	def __init__(self, position = Hallways.TRIFURC):
		self.position = MazeComponent(position)
		self.position.adjacent[Directions.BACKWARDS] = None
		self.position.is_choice_room = True
		self.position.depth = 0
		self.position.set_prize_order(self.generate_prize_order())
		self.num_steps = 0	#This stores the number of steps in a certain direction

	def current_type(self):
		return self.position.room_type
	
	#What prize is possible for new_pos?
	def assign_possible_prize(self, new_pos, direction):
		prizes = self.position.prize_order
		if direction == Directions.LEFT:
			new_pos.prize[0] = prizes[0]
		elif direction == Directions.FORWARDS:
			new_pos.prize[0] = prizes[1]
		else:
			new_pos.prize[0] = prizes[2]
			
	#Mark if the new position will get a prize
	def set_has_prize(self, new_pos):
		if new_pos.options != None:		
			rand_num = random() * 100			
			if len(new_pos.options[1]) > new_pos.depth:
				if rand_num < new_pos.options[1][new_pos.depth - 1]:
						#WON!
						new_pos.prize[1] = new_pos.options[0]
			else:
				if rand_num < new_pos.options[1][len(new_pos.options[1]) - 1]:	#Compare with the last item in options[1]
					new_pos.prize[1] = new_pos.options[0]	#WON!
					
	#Scramble the prizes, and throw in a None for no pathway				
	def generate_prize_order(self):
		possible_prizes = ReadFile.get_inventory_types()
		possible_prizes.append(None)
		ordered = []
		for x in range(3):
			random_number = randint(0, len(possible_prizes) - 1)
			ordered.append(possible_prizes[random_number])
			if possible_prizes[random_number] == None:
				possible_prizes.remove(None)	#Prevent more than 1 None
			
		return ordered
	
	#Step in a certain direction. Trifurcation is the default next room.
	def step(self, direction, hall_type = Hallways.TRIFURC):
		if direction not in self.position.adjacent:	#Not visited
			new_pos = MazeComponent(hall_type)
			new_pos.last_pos = self.position
			
			if self.position.is_choice_room:	#In a choice room
				new_pos.is_choice_room = False
				self.assign_possible_prize(new_pos, direction)
				new_pos.depth = 1
				new_pos.options = ReadFile.get_option(new_pos.prize[0])
				self.set_has_prize(new_pos)	#Winner?
			
			else:	#In a `straight' choiceless room
				if direction in [Directions.LEFT, Directions.RIGHT]:	#the user turns
					new_pos.is_choice_room = True
					
					#Determine order o' prizes
					new_pos.set_prize_order(self.generate_prize_order())
					
				elif direction == Directions.FORWARDS:	#User proceeds forward
					#default of is_choice_room is false
					new_pos.prize[0] = self.position.prize[0]
					new_pos.depth = self.position.depth + 1
					new_pos.options = self.position.options
										
					self.set_has_prize(new_pos)	#Winner?
			
			self.position.adjacent[direction] = new_pos	
			
			#Allow yourself to go backwards
			if direction == Directions.FORWARDS:
				new_pos.adjacent[Directions.BACKWARDS] = self.position
			elif direction == Directions.BACKWARDS:
				new_pos.adjacent[Directions.FORWARDS] = self.position
			elif direction == Directions.LEFT:
				new_pos.adjacent[Directions.BACKWARDS] = self.position
			elif direction == Directions.RIGHT:
				new_pos.adjacent[Directions.BACKWARDS] = self.position
				
			self.position = new_pos
		elif self.position.adjacent[direction] != None:
			self.position.adjacent[direction].last_pos = self.position
			self.position = self.position.adjacent[direction]
			self.position.prize = [self.position.prize[0], 0, False]
				
	
	#If the user just won, give the prize. Returns True when prize given
	def give_prize(self, inventory):
		if self.position.prize[1] != 0 and not self.position.prize[2]:
			self.position.prize[2] = True
			inventory.inventory[self.position.prize[0]] += self.position.prize[1]
			self.position.set_prize_order(self.generate_prize_order())
			self.position.is_choice_room = True
			return True
		return False

	def __repr__(self):
		pass
