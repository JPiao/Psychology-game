from Globals import *
import ReadFile
import os

class WriteFile:
	def __init__(self, inventory, maze):
		self.maze = maze
		self.file_name = self.file_name()
		self.inventory = inventory
		self.out_list = []	#This list will be outputted
		
		handle = open(self.file_name, 'w')
		handle.write('DEPTH, LEFT CUE, CENTRE CUE, RIGHT CUE, CHASING CUE, CHOICE, INVENTORY0, INVENTORY1, INVENTORY2, PRIZE, QUANTITY\n')
		handle.close()
		
	'''Get an available file name. Add numbers to the file number until
		it doesn't exist.'''
	def file_name(self):
		name = OUTPUT_FILE
		
		counter = 0
		while os.path.isfile(name):
			path, ext = os.path.splitext(OUTPUT_FILE)
			name = path + str(counter) + ext
			counter += 1
		return name
	
	'''Outputs the following format:
		ROOM NUMBER, LEFT CUE, CENTRE CUE, RIGHT CUE, 
		CHASING CUE, || CHOICE, INVENTORY0, INVENTORY1, 
		INVENTORY2, PRIZE, QUANTITY		
		
		More info in the relevant readme file.'''
	def flush_output(self):
		handle = open(self.file_name, 'a')
		handle.write(','.join(self.out_list) + '\n')
		handle.close()
		self.out_list = []
	
		#FIXME: Choice and prizes
		'''Load everything that can be done before prize given, i.e. 
			until CHASING CUE.'''
	def add_output_buffer_prelim(self):
		position = self.maze.position
		
		#add depth
		self.out_list.append(str(position.depth))
		
		#Add cues
		if position.room_type == Hallways.RIGHT_BIFURC:
			self.out_list.extend(["-1", str(position.prize_order[1]), str(position.prize_order[2])])
		elif position.room_type == Hallways.LEFT_BIFURC:
			self.out_list.extend([str(position.prize_order[0]), str(position.prize_order[1]), "-1"])
		elif position.room_type == Hallways.BIFURC:
			self.out_list.extend([str(position.prize_order[0]), "-1", str(position.prize_order[2])])
		else:
			self.out_list.extend([str(x) for x in position.prize_order])
			
		if position.is_choice_room:
			self.out_list.append("-1")	#Chasing cue
		else:	#Regular room
			self.out_list.append(str(position.prize[0]))	#Chasing cue


		
	'''Load everything that can be done after prize given, i.e. CHOICE
		until the end.'''
	def add_output_buffer_postlim(self):
		position = self.maze.position.last_pos
		
		if position != None:		#Choice
			if position.is_choice_room:
				self.out_list.append(str(self.maze.position.prize[0]))
			else:
				self.out_list.append("-1")
				
		inv_types = ReadFile.get_inventory_types()
		
		self.out_list.extend([str(self.inventory.inventory[inv_types[x]]) for x in range(3)])
		
		if self.maze.position.prize[2]:	#If just got a prize
			self.out_list.extend([str(self.maze.position.prize[0]), str(self.maze.position.prize[1])])
		else:
			self.out_list.extend(['None', 'None'])
