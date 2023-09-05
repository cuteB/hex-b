# Hex Game Rules

> Rules because I hate cheaters.

## Basic Overview

Hex is played on an 11 by 11 play area.
Players take turns placing one of their pieces in the play area.
A player wins by connecting their two end zones. 
The Blue player's two end zones are onn the top and bottom of the board and the red player's end zones are on the left and right sides of the board. 
On a players turn they can claim an empty (white) by placing their coloured piece on it.
Then the turn ends and the other player's turn starts where they claim an empty space.
Once a space is claimed then that space cannot change players.
The game ends once a player has a continuous line of connected spaces that they own that connects their two end zones.
Each player's end zone is a line of claimed pieces and any of the pieces of one end zone can be used to connect any piece of the players end zone on the opposite side of the board. 
Normally the blue player goes first but when playing multiple games in a row the starting player swaps each game.

### Game stages

The explicit stages of the game and rules for each one.

#### Pre game

Setup an empty HexBoard.
The HexBoard is an 11 by 11 board with an 11 by 1 end zone for each player.
The Play area will be completely empty (white) spaces.
Each end zone will be set as player spaces as defined in [the end zone coordinates](#end-zones-coordinates).
Blue will get the first turn unless multiple games are being played, then the player that went second last game will get the first move.

##### Play Area Coordinates

> I think there is a fancy mathematical expression I can use to define these coordinates. For now it will look like python code.

The play area is any `(x,y)` coordinates with `x in range [0,10]` and `y in range [0,10]`

##### End Zones Coordinates

Player | Edge | Coordinate Range
--|--|--
Blue | Top | `{(0, -1) .. (10,-1)}`
Blue | Bottom | `{(0,11) .. (10,11)}`
Red | Left | `{(-1,0) .. (-1,10)}`
Red | Right | `{(11,0) .. (11,10)}`

#### Game Loop

Turns have two phases: The Pre move phase and post move phase. 
The only thing a player can do on their turn is pick an empty spot.
When a player's turn starts, they pick a move, and after they make a move they check if they won. 
Then if the game is still going its then the other player starts their turn. 

##### Pre move

On a players turn they will pick an empty space and put their piece on it. 
If the game is in progress there will always be an empty space available. 

##### Post Move

After the player makes a move, check to see if that player connected their two end zones. 
If they connected their end zones they win and the game is over.
If not then the turn ends and the player switches so the next player starts their turn.

#### End Game

A game ends once a player connects their two end zones with their pieces.
The game is over and that player gets a win. 
If playing multiple games then move to to the pre game setup and swap starting players.
