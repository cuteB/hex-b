# Hex Game Rules

> Rules because I hate cheaters.

## Basic Overview

Hex is played on an 11 by 11 play area.
Players take turns placing one of their pieces in the play area.
A player wins by connecting their two end zones with a line of their adjacent hexes. 
The Blue player's two end zones are on the top and bottom of the board and the red player's end zones are on the left and right sides of the board. 
On a players turn they can claim an empty (white) by placing their coloured piece on it.
Then the turn ends and the other player's turn starts where they claim an empty space.
Once a space is claimed then that space cannot change players.
The game ends once a player has a continuous line of connected spaces that they own that connects their two end zones.
Each player's end zone is a line of claimed pieces and any of the pieces of one end zone can be used to connect any piece of the players end zone on the opposite side of the board. 
Normally the blue player goes first but when playing multiple games in a row the starting player swaps each game.

### Game Board

The [HexBoard](./Board.md) has a [play area](./Board.md#play-area-coordinates) and [end zones](./Board.md#end-zones).
Each game starts with an [empty board](./Board#empty-board)

### Game stages

The explicit stages of the game and rules for each one.

#### Pre game stage

##### Setup an empty HexBoard

The game starts with an [empty board](./Board.md#empty-board)
Blue will get the first turn unless multiple games are being played, then the player that went second last game will get the first move.

#### Game Loop

Turns have two phases: The Pre move phase and post move phase. 
The only thing a player can do on their turn is pick an empty spot.
When a player's turn starts, they pick a move, and after they make a move they check if they won.
Then if the game is still going its then the other player starts their turn. 

##### Pre move

On a players turn they will pick an empty space and put their piece on it. 
If the game is in progress there will always be an empty space available. 

The Pre move phase

##### Post Move

After the player makes a move, check to see if that player connected their two end zones. 
If they connected their end zones they win and the game is over.
If not then the turn ends and the player switches so the next player starts their turn.

#### End Game

A game ends once a player connects their two end zones with their player spaces.
The game is over and that player gets a win. 

A connected line of player spaces is a path returned by the pathfinder that costs 0.
The path consists of only player spaces and no empty spaces.

If playing multiple games then move to to the pre game setup and swap starting players.
