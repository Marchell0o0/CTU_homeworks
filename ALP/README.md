# Short description of every project

## Homeworks folder 

1. Finds the longest non-descending sequence of numbers that in their absolute value aren't primes.
2. Multiplies two decimal or whole nubmers in a chosen numbers system.
3. Converts dates from numbers to words, or from words to numbers
4. Given a big number, puts operations + and * betweeen the digits in a way that the final equation is equal to the other given number.
5. Evaluates if there is a mate, check, garde or nothing on a chess board.
6. Finds the biggest rectangle of negative numbers in a given matrix. 
7. Finds a way to fill up a given field with given pieces. 
8. On a board, finds the fastest way for a horse piece to go from start to goal tile.
9. Code: codes up a string into a set of big numbers. Attack: given a coded message and a set of words from which at least one word should be present in the message, tries every e value from 2^18 to 2^20 to find the right decoded version.

## TRAX

### Test run
The final version of the player is player3.0, which uses minimax with alpha-beta. If you run the program, a game will be played between two instances of that player, and the screenshots of every move will be put in a folder Moves. 

### Version progression
When testing the program using a profiler, the biggest time spent was on the evaluation function, because of the rules of the game a player gets points equal to the length of a cycle or a line that goes from one side to the opposit of their color. So everytime to evaluate if the game ended or how many points you get after any route you have to check if there is a cycle from every tile(almost) and if there is a line from every edge tile. And all of that for both colors.

Final version doesnt use MCTS because stupid decisions are made as if using random propagation there is not enough time for the algorithm to see that its about to lose in two moves. For that I've tried to implement minimax for propagation phase, where when propagating it chooses a move from a minimax with depth 2, but that only made things even slower so no real deep evaluation was made.

# Testing 

If the program doesnt need any external files just run and input something that makes sense. If the file is needed you can create it yourself, even though you couldn't test the sixth program properly because you need a really big matrix for that.
