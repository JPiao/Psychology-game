'''Pass in the inventory item. This function will do something when 
	the user dies (or not!)
	
	I have designed some friendly helper functions that may come in 
	handy when making a good death message.
	'''
from Output2d import *
from Globals import *

class Dead:
	def __init__(self, output2d, time, writefile):
		self.output2d = output2d
		self.time = time
		self.writefile = writefile
	
	'''This function just writes your message to the end of the output file.
	NB you probably don't need to say too much technical info, because all the
	data is the same as from the last record in the file.'''
	
	def write_to_file(self, string):
		handle = open(self.writefile.file_name, 'a')
		handle.write(string + '\n')
		handle.close()
		
	def death(self, item):
		'''Use output2d.draw_centred(message, side_padding = 1, up_padding = 1)
		for text'''
		
		close_program = False
		
		if item[0]:
			self.output2d.draw_centred('You died')
			self.time.reset()	#So we don't count previous timing in the following delay:
			self.time.mri_delay(DEATH_DELAY)
			self.write_to_file('Died from inventory type no. 1')
			close_program = True
			# died from item 0
			
		if item[1]:
			pass	#Do nothing
			# died from item 1
			
		if item[2]:
			pass	#Do nothing
			# died from item 1
			
		if close_program:
			quit(0)	#END GAME!
