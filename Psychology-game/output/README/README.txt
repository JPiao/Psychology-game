DEPTH, LEFT CUE, CENTRE CUE, RIGHT CUE, CHASING CUE, CHOICE, INVENTORY0, INVENTORY1, INVENTORY2, PRIZE, QUANTITY
.
.
.
--------------------------------------------------
N.B. that these headers will appear in each output file. The name of the output files is specified in Globals.py. Orders of inventory correspond to the order that was given in the input file, from 0. As well, information regarding each room is only written to file *after* one has left the room.

DEPTH records the number of steps from a room with choices.

LEFT CUE, CENTRE CUE, RIGHT CUE denote what cues appear at each position. "None" will appear if no cue is given or the user is in a regular, choiceless room. "-1" is written if where is a wall.

CHASING CUE is the cue the person is trying to get. "None" indicates the user is chasing after nothing or has gone backwards. "-1" indicates the user is in a room with choices. When the user gets a prize, this is equal to PRIZE.

CHOICE represents what the user chose in a room with choice. If the user is not in a choice room, this value is -1. If the user chooses nothing or goes backwards, the value is "None".

INVENTORY0, INVENTORY1, INVENTORY2 are the the respective amounts of inventory the user has. This value is recorded after a prize is given.

PRIZE is the type of prize the user just recieved. "None" if no prize recieved.

QUANTITY is the amount of prize just recieved. "None" if no prize recieved.
