from MazeComponent import *
from Globals import *
import ReadFile
from random import random, randint
from User import *

class Maze:	
	#Pass in maze dimensions
	def __init__(self):
		self.position = MazeComponent(Hallways.TRIFURC)
		self.position.adjacent[Directions.BACKWARDS] = None
		self.position.is_choice_room = True
		self.position.depth = 0
		
		self.position.set_prize_order(self.generate_prize_order(self.position))
		self.num_steps = 0	#This stores the number of steps in a certain direction
		self.total_step_count = 0	#Total number of steps.

	def current_type(self):
		return self.position.room_type
	
	#What prize is possible for new_pos?
	def assign_possible_prize(self, new_pos, direction):
		prizes = self.position.prize_order
		#print(prizes, 'here are the prizes in prize order')
###########MAYBE THE ISSUE IS HERE BECAUSE THE PRIZES GET SET HERE for the new pos????
		if direction == Directions.LEFT:
			new_pos.prize[0] = prizes[0]
			new_pos.options = self.position.prize_infos[0]
		elif direction == Directions.FORWARDS:
			new_pos.prize[0] = prizes[1]
			new_pos.options = self.position.prize_infos[1]
		else:
			new_pos.prize[0] = prizes[2]
			new_pos.options = self.position.prize_infos[2]
			
	#Mark if the new position will get a prize
	def set_has_prize(self, new_pos):
		#if new_pos.options != [] and new_pos.options is not None: #it equalled [] so maybe it was the wrong check ie =None???	
		if new_pos.options is not None:
			print ('new pos option:', new_pos.options)
			#print ('new pos type:', type(new_pos.options[3]))
			print ('new pos depth:', new_pos.depth)
			rand_num = random() * 100	
			if len(new_pos.options[3]) >= new_pos.depth:
				#print rand_num, new_pos.options[3][new_pos.depth - 1]
				if rand_num < new_pos.options[3][new_pos.depth - 1]:
						#WON!
						#print 'won'
						new_pos.prize[1] = new_pos.options[1]
			else:
				if rand_num < new_pos.options[3][len(new_pos.options[3]) - 1]:	#Compare with the last item in options[1]
					new_pos.prize[1] = new_pos.options[1]	#WON!
					
	#Scramble the prizes, and throw in a None for no pathway				
	def generate_prize_order(self, position):
		print 'Prize infos: '  + str(position.prize_infos)
		lis = []
		for inf in position.prize_infos:
			if inf:
				lis.append(inf[0])
			else:
				lis.append(None)
		return lis
	
	#Step in a certain direction. Trifurcation is the default next room.
	#Choice_room is true if you want a cboice room. This only works if you 
	#are leaving a straight room
	def step(self, direction, choice_room = False):
		if direction not in self.position.adjacent:	#Not visited
			new_pos = MazeComponent(Hallways.STRAIGHT)
			new_pos.last_pos = self.position
			if self.position.is_choice_room:	#In a choice room
				new_pos.is_choice_room = False
								
				self.assign_possible_prize(new_pos, direction)
				new_pos.depth = 1
				#print 'Got to get option'
				#new_pos.options = ReadFile.get_option(new_pos.prize[0])
				print 'Options: ' + str(new_pos.options)
				self.set_has_prize(new_pos)	#Winner?
				
				new_pos.set_prize_order(self.generate_prize_order(new_pos))
				
				new_pos.prize_order[1] = None	#Centre column is none because you already followed a prize (this does not apply to first choice room)
				new_pos.prize_infos[1] = None
				print('i got here1')

			else:	#In a `straight' choiceless room
				if direction in [Directions.LEFT, Directions.RIGHT]:	#the user turns
					new_pos.is_choice_room = False
					
					#Determine order o' prizes
					new_pos.set_prize_order(self.generate_prize_order(new_pos))
					
					new_pos.prize_order[1] = None#Centre column is none
					new_pos.prize_infos[1] = None
					
					self.assign_possible_prize(new_pos, direction)
					new_pos.depth = 1
					#new_pos.options = ReadFile.get_option(new_pos.prize[0])
					
					self.set_has_prize(new_pos)	#Winner?
					print('i got here2')
				elif direction == Directions.FORWARDS:	#User proceeds forward
					#default of is_choice_room is false
					new_pos.prize[0] = self.position.prize[0]
					print("PRIZE0", self.position.prize)
					new_pos.depth = self.position.depth + 1
					new_pos.options = self.position.options

					new_pos.set_prize_order(self.generate_prize_order(new_pos))
					
					new_pos.prize_order[1] = None	#Centre column is none
					new_pos.prize_infos[1] = None
					
					self.set_has_prize(new_pos)	#Winner?
					print('i got here3')			
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
		#still for going backwards	
		elif self.position.adjacent[direction] != None:
			self.position.adjacent[direction].last_pos = self.position
			self.position = self.position.adjacent[direction]
			self.position.prize = [self.position.prize[0], 0, False]
			print("PRIZE1", self.position.prize)
				
	
	#If the user just won, give the prize. Returns True when prize given
	def give_prize(self, inventory):
		print("PRIZE2", self.position.prize)
		if self.position.prize[1] != 0 and not self.position.prize[2]:
			self.position.prize[2] = True
			inventory.give_prize(self.position.prize[0], self.position.prize[1])
			self.position.set_prize_order(self.generate_prize_order(self.position))
			self.position.is_choice_room = True
			self.position.depth = 0
			return True
		return False
		
	#Increase step count so we know how much inventory to remove
	def increment_step_count(self):
		self.total_step_count += 1
