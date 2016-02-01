import pygame

#Define the event loop
def event_loop():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:	#Quit if you leave the window
			pygame.quit()
			quit()
		elif pygame.key.get_pressed()[pygame.K_ESCAPE]:#or quit with esc key
			pygame.quit()
			quit()		
#Wait for key to be lifted to continue
def wait_key_up(key):	
	#GLComponents.hallway(maze.current_type(), True, maze.position.colours)							
	#pygame.display.flip()
	
	while pygame.key.get_pressed()[key]:
		event_loop()
