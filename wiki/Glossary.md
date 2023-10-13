# Glossary

> At some point, someone other than me will read this repo and you gonna think "Wow, this guy can write markdown"

## Adjacent Hex

A hex that is beside one of the players existing hexes. Could also be an Opponent's Adjacent Hex if its a hex beside one of their hexes, or perhaps a conflict Adjacent hex if it is between one of your and your opponent's hexes.

## Satellite Hex

An empty hex that is adjacent to a player's Adjacent Hexes

## Middle Move

Moves that can be used to connect hex groups that can't be easily blocked because it takes the opponent multiple turns to block the path to that hex. (probs need a picture/example later)

## Strong Move

A move that is two spaces away with two possible moves to bridge the gap ([Bridge Move](#bridge-move)). Moves like this are essentially moving two spaces with one move because if your opponent takes one of the bridge moves, b<sup>1</sup>, then your next move is the the other bridge move, b<sup>2</sup>. The result is no change real change in board state.

![Strong Move Example](/wiki/zImages/patterns/strong-move.png)

### Bridge Move

A move that is in between a strong move. These can be further defined as your bridge move (if it is your strong move) and your opponent's bridge move (their strong move). Bridge moves will come in pairs and be labeled as sibling bride moves. This is basically the same as a [strong connection](#Strongly-Connected) but a bridge move is monitored and taken when it is changed into a weak connection.

## Connections

Connections are about connecting a player's hexes to each other. A few types:

- ### Connected

    Moves of a player are touching. No need to connect them they already touching each other enough. Moves than connect a player's moves are connection moves

- ### Strongly Connected

    These are moves that are connected by at least two hexes. Strongly connected because the opponent shouldn't be able to separate them (if the agent is smart). Checkout [Strong Moves](#strong-move)

- ### Weakly Connected

    Moves that are connected by a single empty hex. Just like yo girl, these gonna be taken by the opponent if you don't take them on your turn.

- ### Not Connected

    Gotta write a definition because some of you are bad at the game. These moves are not even close to being connected. Need at least two moves to connect them to each other. Unless you the 43rd generation of my best agent you shouldn't even bother making moves that are not connected.
