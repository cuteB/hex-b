# AgentSmart

> Work smarter not harder.

## Summary

The biggest goal I want to accomplish with this agent is the ability to detect [strong moves](#strong-move). I want this agent actually make strong moves, not to bridge the gap between strong moves until endgame, and then detect when the opponent takes up one of the [bridge moves](#bridge-move) and then always take the other bridge on the move after. It is also important to know when it is beneficial to make an opponent's bridge move for your own position.

> If AgentSmart only cares about strong moves what does AgentStrong care about?

## Game Plan

---

AgentSmart's game plan will be three parts: early, mid, late game. These stages will be as follows

- **Early game** Make the best first move. Super simple. I don't want to over complicate this agent's strategy apart from strong moves. For now this may be pretty hard coded and put a move closest to the center.
- **Mid game** Building off of the starting move with strong moves that build an area of control. Identifying when an opponent makes one of our bridge move and our next move is taking the sibling bridge move.
- **End game** When our board state is "won" with strong moves connecting both of our ends. Simply take our own bridge moves to connect our hexes to win the game.

### Get Strong Moves

Given a board state, get all strong moves for a player. For now just identify what moves are good, don't need to evaluate them just yet.

1. Need to "init agent board" where agent grabs all moves from the game board. (Speed up operations)
1. Get [adjacent hexes](#adjacent-hex) in the current board state. Next grab the hexes around all of the adjacent hexes and put in a count for each of the adjacent hexes touching it. Hexes with more than one hex is considered a strong move.
1. Strong Moves will need to be evaluated to check if it increases board value. Moves with no increase in board value will be pruned.

#### Strong Move Example Notes

![Strong Move Evaluation](/wiki/images/resize.png)]

- Need to count based off of a single hex. Hexes with 2 (D) or 3 (C) from different hexes aren't that strong because they can be easily blocked.
- Hexes with 4 (E) are very strong if they create 2 sets of strong moves. Need to change up evaluation based on previous point.
- If an adjacent move is touching the end zone, it shouldn't be used to count strong moves. No point in evaluating them when the adjacent move can be used to connect to the end zone. May need to come back and check if the adjacent move can be blocked or whatever.
- Moves such as (B) can't be easily blocked by the opponent so they can be used as [middle moves](#middle-move). I could make move (A). This move may not look the best because the opponent can go to the left of it and block it from that strongly connected hex group. I would then take (B) because it is still a strong move because having a value of 3 instead of 2 means it takes the opponent 3 turns to block it from connecting.
- **Strong moves that flow with the board short ways rather than long ways are more valuable.**

### Get Strong Moves Implementation

> "Stronger than Yesterday" - Rock Lee

Given a board state the function should return all of the moves that are strong.

#### Strong Move Tests

Simple cases

- Single hex, simple
- Multiple single hexes
- one group of hexes
- multiple group of hexes
- Bunch of single hexes
- Bunch of groups of hexes

## Glossary

---

### Adjacent Hex

A hex that is beside one of the players existing hexes. Could also be an Opponent's Adjacent Hex if its a hex beside one of their hexes, or perhaps a conflict Adjacent hex if it is between one of your and your opponent's hexes.

### Middle Move

Moves that can be used to connect hex groups that can't be easily blocked because it takes the opponent multiple turns to block the path to that hex. (probs need a picture/example later)

### Strong Move

A move that is two spaces away with two possible moves to bridge the gap ([Bridge Move](#bridge-move)). Moves like this are essentially moving two spaces with one move because if your opponent takes one of the bridge moves, B<sup>1</sup>, then your next move is the the other bridge move, B <sup>2</sup>. The result is no change real change in board state.

![Strong Move Example](/wiki/images/strong-move.png)

#### Bridge Move

A move that is in between a strong move. These can be further defined as your bridge move (if it is your strong move) and your opponent's bridge move (their strong move). Bridge moves will come in pairs and be labeled as sibling bride moves
