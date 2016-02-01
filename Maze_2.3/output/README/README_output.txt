COUNT, DEPTH, LEFT CUE, CENTRE CUE, RIGHT CUE, LVALUE, LIMAGE, LPROBS, CVALUE, CIMAGE, CPROBS, RVALUE, RIMAGE, RPROBS, CHASING CUE, CHOICE, DIRECTION, INVENTORY0, INVENTORY1, INVENTORY2, PRIZE0, PRIZE1, PRIZE2, DEC0, DEC1, DEC2
.
.
.
--------------------------------------------------
N.B. that these headers will appear in each output file. The name of the output files is specified in Globals.py. Orders of inventory correspond to the order that was given in the input file, from 0. As well, information regarding each room is only written to file *after* one has left the room.

COUNTER simply counts up from zero.

DEPTH records the number of steps from a room with choices. NB if one is in a hallway while chasing something and turns, it considers the depth to be 1, because the user still chose what to chase after.

LEFT CUE, CENTRE CUE, RIGHT CUE denote what cues appear at each position. "None" will appear if no cue is given or the user is in a regular, choiceless room. "-1" is written if where is a wall.

LVALUE...RPROBS are the value for each prize you could get, the image file and the list of probabilities associated with the left, centre and right cues respectively.

CHASING CUE is the cue the person is trying to get. "None" indicates the user is chasing after nothing or has gone backwards. "-1" indicates the user is in a room with choices. When the user gets a prize, this is equal to PRIZE.

CHOICE represents what the user chose in a room with choice. If the user chooses nothing or goes backwards, the value is "None".

DIRECTION is the key pressed by the user.

INVENTORY0, INVENTORY1, INVENTORY2 are the the respective amounts of inventory the user has. This value is recorded after a prize is given.

PRIZE0, PRIZE1 and PRIZE2 represent the amounts of each prize just recieved (if any). 

DEC0, DEC1, DEC2 indicate how much of each respective inventory type was lost by taking steps.
