from Globals import *
import GLComponents
import random
import ReadFile

class MazeComponent:
	'''
	Fields:
	-------
	adjacent
	room_type
	is_choice_room
	colours
	depth
	prize[inventory type, amount, given]
	prize_order[prize1, prize2, prize3]
	options 
	last_pos
	prize_infos[option1,option2,option3]
	'''
	
	def generate_room(self):#may not be used
		return random.randint(0, 6) 
	
	#Add an adjacent maze component in a certain direction
	def add_adjacent(self, direction, instance):
		self.adjacent[direction] = instance
		
	'''room_type is the type of room this component is (Hallways type). 
	colours is a list of colour triplets to indicate the wall colours.
	is_choice_room is true if the user is to make a decision about where
		to turn (versus going on a straight trek). 
	prize is a list whose first item is the inventory type, the second is the amount
		and the third is if it has been distributed yet. 
	prize_order contains the prizes in order, when is_choice_room = True. 
	options is the options given by ReadFile.??
	las_pos is simply the last visited position before getting here. 
	prize infos contains the three option info from the read file'''

	def __init__(self, room_type = None, colours = None, is_choice_room = False, 
		possible_prize = None, prize = None, depth = 0, options = None,
		last_pos = None):
		self.adjacent = {}
		self.room_type = room_type
		self.is_choice_room = is_choice_room
		if prize == None:
			self.prize = [None, 0, False]
		else:
			self.prize = prize
			
		
		self.depth = depth
		self.options = options
		
		if colours == None:
			self.colours = self.generate_colours(self.room_type)
		else:
			self.colours = colours
		
		self.last_pos = last_pos
		self.prize_infos = [ReadFile.get_option() for x in range(3)] 	#This contains three instances of ReadFile.get_option(). 
		self.prize_infos[1] = None #overwrite middle one so now cue in centre
		#This is just a detailed version of prize_order. In fact, prize order only exists
		#since it was made before prize_info was needed, and it is now hard to remove.

		self.prize_order = [None, None, None]
		
	#Generate colours
	@staticmethod
	def generate_colours(room_type):
		return [[random.random()/2 for x in range(3)] for x in range(GLComponents.num_colours[room_type])]
		
	#Sets the order of prizes. Also changes the type of hallway 
	#appropriately
	def set_prize_order(self, prize_order):
		self.prize_order = prize_order
		#print(prize_order, 'this is the prize order')
#		if prize_order[0] == None:
#			self.room_type = Hallways.RIGHT_BIFURC
#		elif prize_order[1] == None:
#			self.room_type = Hallways.BIFURC
#		elif prize_order[2] == None:
#			self.room_type = Hallways.LEFT_BIFURC
#		else:
#			self.room_type = Hallways.TRIFURC
#		if random.random() < 0.5:
#			self.room_type = Hallways.TRIFURC
		self.room_type = Hallways.TRIFURC #added this so its always trifurcs?
		self.colours = [[random.random()/2 for x in range(3)] for x in range(GLComponents.num_colours[self.room_type])]
		
	def __repr__(self): #helps with debugging somehow
		return str("\tType: " + str(self.room_type) + "\n\tAdjacents: " + str([x for x in self.adjacent]))
