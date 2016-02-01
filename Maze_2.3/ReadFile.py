from Globals import *
import random
'''This file has functions that read in files. To optimize, if need be,
make sure these only run once, and save the contents of files globally.
Make this all into a class. '''

inventory_types = []	
minimums = []
cap = []
count = 0

#Cleans a string read from file, turns it into a list (comma-seperated)
def clean_list(string):
	return string.strip().replace(' ', '').split(',')

'''Returns inventory types specified in the first line of the files. This
	is the ``official order''.'''
def get_inventory_types():
	global inventory_types, count
	count += 1
	if inventory_types != []:
		return inventory_types[:]
	else:
		handle = open(INPUT_FILE, 'r')
		a = clean_list(handle.readline())
		handle.close()
		inventory_types = a[:]
		return a
		
'''Return a list of the minimums of each inventory type. In ``official
order.''.'''
def get_mins():
	global minimums
	if minimums != []:
		return minimums##############WHAts this bit here for?
	else:
		handle = open(INPUT_FILE, 'r')
		handle.readline()
		a = clean_list(handle.readline())
		handle.close()
		minimums = [float(x) for x in a]
		return minimums

print get_mins()

'''Return a list of the initial values of each inventory type. In ``official
order.''.'''
def get_init_inv_vals():
	#global init_inv_vals #?????????????
	#if init_inv_vals != []:
	#	return init_inv_vals #IT didn't like this because it sayd global name .. is not defined
#	else:
	handle = open(INPUT_FILE, 'r')
	handle.readline() 
	handle.readline() #ignore 1st 2 lines
	a = clean_list(handle.readline())
	handle.close()
	init_inv_vals = [float(x) for x in a]
	return init_inv_vals


'''Selects a random inventory item based on values given in INPUT_FILE
from Globals.py. Returns a list with the following:
inventory type
quantity
image location (no folder)
list of probabilities for winning. The last index is maintained ad. inf.
'''
def get_option():
	handle = open(INPUT_FILE, 'r')
	handle.readline()	#Ignore first line
	handle.readline()	#Ignore 2nd line
	handle.readline()	#ignore 3rd line
	lines = handle.read().strip().split('\n')
	handle.close()
	
	total = 0
	rand_percent = random.randint(1, 100)
	chosen = None
	for line in lines:
		line = clean_list(line)
		total += float(line[1])
		if rand_percent <= total:
			chosen = line
			break
	
	if chosen:	#Not None
		chosen = [chosen[0], float(chosen[2]), chosen[3], [float(x) for x in chosen[4:]]]
	return chosen

'''a = {'food':0, 'water':0,'money':0,'None':0}
for x in range(1000):	
	val = get_option()
	if val:
		a[val[0]] += 1/1000.0
print a'''


'''Choose a line from INPUT_FILE based on the probabilities. Pass in an 
inventory type, and the function will return (in order):
How much of the type
A list of the probabilities after each step

If the function returns None, there is no result.
''''''
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
		print chosen_option[1:][1]
		return chosen_option[1:]	'''
		
#Read the waiting times for hallways
def read_times():	
	handle = open(STR_TIMES, 'r')
	times = handle.readline().split(' ')
	handle.close()
	return [float(n) for n in times]

'''Read in the decrementation info. The nth array in the returned array
represents the nth inventory item. THe two values in the sub arrays are,
respectively, the frequency of decrement and the amount to decrement by.'''
def read_decrement():
	handle = open(DECREMENT_FILE, 'r')
	lines = handle.read().strip().split('\n')
	lines = [clean_list(line) for line in lines]
	handle.close()
	return [map(float, x) for x in lines]

'''Return a list of the caps of each inventory item'''
def read_caps():
	global cap
	if cap == []:
		handle = open(CAPS_FILE, 'r')
		line = handle.read().strip().split(',')
		handle.close()
		cap = [float(x.replace(' ', '')) if x.replace(' ', '') != '' else None for x in line]
	return cap[:]
