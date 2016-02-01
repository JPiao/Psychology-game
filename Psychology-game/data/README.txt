TODO: To implement a function for probability with a distribution

INVENTORY TYPES
PERCENT FOR THIS OPTION, NUMBER, PROB. OF OUTCOME
PERCENT FOR THIS OPTION, NUMBER, PROB. OF OUTCOME

PERCENT FOR THIS OPTION, NUMBER, PROB. OF OUTCOME
PERCENT FOR THIS OPTION, NUMBER, PROB. OF OUTCOME
.
.
.
--------------------------------------------------

The first line is a list of "inventory types", e.g. food, water, money. 

The next sections are seperated by an empty line. The nth block corresponds to the nht inventory tpye.

PERCENT FOR THIS OPTION. This is the chance that this line is chosen at a given point in the maze. The sum of percents must be <= 100 in each block; if they add to x < 100, there is a 100 - x chance the person will get nil. This is equivalent to setting "PERCENT FOR THIS OPTION" or "PROB. OF OUTCOME" to 0. 

NUMBER. How must of the object will you get? This is a real number.

PROB. OF OUTCOME. A period-separated list of percents representing the probability of getting the object. The nth position represents the nth step. In a list of m numbers, the mth percent is assumed for all steps > m.

--------------------------------------------------
EXAMPLE FILE:
food, water, money
10, 3, 10. 20. 30. 40. 50
30, -0.5, 1. 1. 1. 100
60, 2, 100

40, 5, 50. 0
10, 0.8, 50. 30. 10

10, 10, 50. 60. 70. 80. 100
70, 1, 2. 5. 10
