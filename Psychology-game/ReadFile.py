from Globals import *
import random

#Cleans a string read from file, turns it into a list (comma-seperated)
def clean_list(string):
	return string.strip().replace(' ', '').split(',')

'''Returns inventory types specified in the first line of the files. This
	is the ``official order''.'''
def get_inventory_types():
	handle = open(INPUT_FILE, 'r')
	a = clean_list(handle.readline())
	handle.close()
	return a

'''Choose a line from INPUT_FILE based on the probabilities. Pass in an 
inventory type, and the function will return (in order):
How much of the type
A list of the probabilities after each step

If the function returns None, there is no result.
'''
def get_option(inv_type):
	rand_percent = random.random() * 100
	
	handle = open(INPUT_FILE, 'r')
	handle.readline()	#ignore first line
	
	options = []
	
	counter = 0
	inv_types = get_inventory_types()

	if inv_type not in inv_types:
		if inv_type == None:
			return [0, [0]]
		else:
			raise ValueError(str(inv_type) + ' is not listed in ' + INPUT_FILE)	#Check if erronious inventory type passed in
	
	index = [i for i,x in enumerate(inv_types) if x == inv_type]	#Find which inventory type was passed in, as an index
	
	while True:
		line = handle.readline()
		if line in ['\r\n', '\n']:
			counter += 1
			line = handle.readline()
		
		if line == '':	#Done loop
			break
			
		if counter in index:	#Counter equals index?
			listed_line = clean_list(line)
			options.append(listed_line)
				
	if sum([float(x[0]) for x in options]) > 100:
		raise ValueError('The sum of probabilities for ' + inv_type + ' is ' + 
			str(sum([float(x[0]) for x in options])) + '% > 100%')	#Check if error
	
	chosen_option = None
	total = 0	#Choose a line at random
	for line_num in range(len(options)):
		total += float(options[line_num][0])
		if total > rand_percent:
			chosen_option = options[line_num]
			break
	
	
	if chosen_option == None:
		return None
	else:
		chosen_option[1] = float(chosen_option[1])
		chosen_option[2] = chosen_option[2].rstrip('.').split('.')
		for x in range(len(chosen_option[2])):
			chosen_option[2][x] = float(chosen_option[2][x])
			if chosen_option[2][x] > 100:
				raise ValueError('The probability of winning is ' + str(chosen_option[2][x]) + ' > 100%')
			
		return chosen_option[1:]		
