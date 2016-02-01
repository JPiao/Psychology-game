from Globals import *
import ReadFile
import os

class WriteFile:
	def __init__(self, maze):
		self.maze = maze
		self.file_name = self.file_name()
		self.out_list = []	#This list will be outputted
		
		handle = open(self.file_name, 'w')
		handle.write('COUNT, DEPTH, LEFT CUE, CENTRE CUE, '+
			'RIGHT CUE, LQUANTITY, LIMAGE, LPROBS,  CQUANTITY, CIMAGE, CPROBS, '+
			'RQUANTITY, RIMAGE, RPROBS, CHASING CUE, CHOICE, DIRECTION, INVENTORY0,' +
			' INVENTORY1, INVENTORY2, PRIZE0, PRIZE1, PRIZE2, DEC0, DEC1, DEC2\n')
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
		
		self.out_list.append(str(self.maze.total_step_count))	#Add counter
		
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
			
		info = position.prize_infos	#Prize info
		str_info = []
		for x in info:
			if x:
				if type(x) is list:
					for y in x[1:]:	#Remove first item
						if type(y) is list:
							str_info.append('"' + ','.join([str(item) for item in y]) + '"')
						else:
							str_info.append(str(y))
				else:
					str_info.append(str(x))
			else:
				str_info.extend(['None', 'None', 'None'])

		self.out_list.extend(str_info)
			
		if position.is_choice_room:
			self.out_list.append("-1")	#Chasing cue
		else:	#Regular room
			self.out_list.append(str(position.prize[0]))	#Chasing cue


		
	'''Load everything that can be done after prize given, i.e. CHOICE
		until the end.'''
	def add_output_buffer_postlim(self, direction, current_inventory, decrement_amounts):
		position = self.maze.position.last_pos
		
		if position != None:		#Choice
			if position.is_choice_room:
				self.out_list.append(str(self.maze.position.prize[0]))
			else:
				self.out_list.append("-1")
		
		self.out_list.append(direction)	#Direction chosen
				
		inv_types = ReadFile.get_inventory_types()
		
		self.out_list.extend([str(current_inventory[inv_types[x]]) for x in range(3)])	#Inventory
		

		for x in inv_types:
			if x == self.maze.position.prize[0]:
				self.out_list.append(str(self.maze.position.prize[1]))
			else:
				self.out_list.append('0')
				
		self.out_list.extend([str(x) for x in decrement_amounts])
		
