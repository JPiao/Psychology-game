from Globals import *
import ReadFile
import os

chosen_direction = '' #this will get updated everytime you make a new choice
chasing_infos = ['None', 'None', 'None', 'None'] #will update for last thing you chose to follow
str_infos = []

class WriteFile:
	def __init__(self, maze, subject_num=''):
		self.maze = maze
		self.file_name = self.file_name(subject_num)
		self.out_list = []	#This list will be outputted
		
		handle = open(self.file_name, 'w')
		handle.write('SUBJECT, COUNT, DEPTH, L_CUE_TYPE, LVALUE, LIMAGE, LPROBS, ' + 
			'C_CUE_TYPE, CVALUE, CIMAGE, CPROBS, '+
			'R_CUE_TYPE, RVALUE, RIMAGE, RPROBS, DIRECTION, ' +
			'CHOSEN_CUE_TYPE, CHOSEN_VALUE, CHOSEN_IMAGE, CHOSEN_PROBS, ' +
			'PRIZE, DECREASE, CURR_INVENTORY\n')
		handle.close()
		
	'''Get an available file name. Add numbers to the file number until
		it doesn't exist.'''
	def file_name(self, subject_num=''):
		path, ext = os.path.splitext(OUTPUT_FILE)
		name = path + subject_num + ext

		counter = 1
		while os.path.isfile(name):
			path, ext = os.path.splitext(OUTPUT_FILE)
			name = path + subject_num + '_' + str(counter) + ext
			counter += 1
		return name
	
	'''Outputs the following format:
		ROOM NUMBER, LEFT CUE, CENTRE CUE, RIGHT CUE, 
		CHASING CUE, || CHOICE, INVENTORY0, INVENTORY1, 
		INVENTORY2, PRIZE, QUANTITY		
		
		More info in the relevant readme file.'''
	def flush_output(self, subject_num):
		handle = open(self.file_name, 'a')
		handle.write(','.join(self.out_list) + '\n')
		handle.close()
		self.out_list = []

	'''Converts e.g. ['money', 1.0, 'money3.jpg', [0.0, 100.0]] to 
		['money', '1.0', 'money3.jpg', '"0.0,100.0"'] 
		for one direction, not full prize infos, which is a list of lists.'''
	def prize_info_to_string(self, info): 
		str_info = []
		if info is not None:
			for item in info:
				if type(item) is list:
					str_info.append('"' + ','.join([str(item) for item in item]) + '"')	
				else:
					str_info.append(str(item))
		else:
			str_info.extend(['None', 'None', 'None', 'None'])
		return str_info

		'''Load everything that can be done before prize given, i.e. 
			until CHASING CUE.'''
	def add_output_buffer_prelim(self, subject_num):
		self.out_list.append(str(subject_num))	#add sub num, typed in terminal

		position = self.maze.position
		
		self.out_list.append(str(self.maze.total_step_count))	#Add counter
		
		#add depth
		self.out_list.append(str(position.depth))

		info = position.prize_infos	#Prize info
		global str_infos
		str_infos = [] #just to convert to a list of strings, instead of a list of list of stuff
		for dirn in info: #left centre right
			str_infos.extend(self.prize_info_to_string(dirn))
		print('str_infos:', str_infos)
		str_infos[4:8] = chasing_infos #update centre dirn to say what you are chasing from previous turns (if got prize, then its Nones)
		self.out_list.extend(str_infos)
			
#		if position.is_choice_room:
#			self.out_list.append("-1")	#Chasing cue ???????????????????
#		else:	#Regular room
#			self.out_list.append(str(position.prize[0]))	#Chasing cue ???
#			print('position prize' + str(position.prize))
#			print('prize infos in write file' + str(info))
#		
		
	'''Load everything that can be done after prize given, i.e. CHOICE
		until the end.'''
	def add_output_buffer_postlim(self, direction, current_inventory, decrement_amounts):
				
		position = self.maze.position.last_pos
		
#		if position != None:		#Choice
#			if position.is_choice_room:
#				self.out_list.append(str(self.maze.position.prize[0]))
#			else:
#				self.out_list.append("-1")

		global chosen_direction, chasing_infos, str_infos
		chosen_direction = direction #for updating centre/chasing infos later

		self.out_list.append(direction)	#Direction chosen
		
		#to update chasing info for next turn (ie what you just selected) and output the infos of the current chosen direction to file
		if direction == 'left': 
			chasing_infos = self.prize_info_to_string(position.prize_infos[0])
			self.out_list.extend(str_infos[0:4])
		elif direction == 'right':
			chasing_infos = self.prize_info_to_string(position.prize_infos[2])
			self.out_list.extend(str_infos[4:8]) 
		elif direction == 'centre' and self.maze.position.prize.count(None) != len(self.maze.position.prize):  #if centre, don't update, unless prize given, then update to nones
			chasing_infos = ['None', 'None', 'None', 'None']
			self.out_list.extend(str_infos[0:4])


		inv_types = ReadFile.get_inventory_types()
		#for prize and decrease
		for x in inv_types:
			if x == self.maze.position.prize[0]:
				self.out_list.append(str(self.maze.position.prize[1]))
			else:
				self.out_list.append('0')				
		self.out_list.extend([str(x) for x in decrement_amounts])

		self.out_list.extend([str(current_inventory[inv_types[x]]) for x in range(len(inv_types))])	#Inventory	
		
