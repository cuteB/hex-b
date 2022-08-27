# AgentSmart

> Work smarter not harder.

- [Game Plan](#game-plan)
  - [Strong Moves](#get-strong-moves)
  - [Connections](#get-connections)
  - [Smart Chain](#smart-chain)
- [Review](#review)
  - [Issues](#agent-issues)

## Summary

The biggest goal I want to accomplish with this agent is the ability to detect [strong moves](/wiki/Glossary.md#strong-move). I want this agent to make strong moves, not to bridge the gap between strong moves until endgame, detect when the opponent takes up one of the [bridge moves](/wiki/Glossary.md/#bridge-move) and then always take the other bridge on the move after. It is also important to know when it is beneficial to make an opponent's bridge move for your own position.

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
1. Get [adjacent hexes](/wiki/Glossary.md#adjacent-hex) in the current board state. Next grab the hexes around all of the adjacent hexes and put in a count for each of the adjacent hexes touching it. Hexes with more than one hex is considered a strong move.
1. Strong Moves will need to be evaluated to check if it increases board value. Moves with no increase in board value will be pruned.

#### Strong Move Example Notes

![Strong Move Evaluation](/wiki/images/resize.png)

- Need to count based off of a single hex. Hexes with 2 (D) or 3 (C) from different hexes aren't that strong because they can be easily blocked.
- Hexes with 4 (E) are very strong if they create 2 sets of strong moves. Need to change up evaluation based on previous point.
- If an adjacent move is touching the end zone, it shouldn't be used to count strong moves. No point in evaluating them when the adjacent move can be used to connect to the end zone. May need to come back and check if the adjacent move can be blocked or whatever.
- Moves such as (B) can't be easily blocked by the opponent so they can be used as [middle moves](/wiki/Glossary#middle-move). I could make move (A). This move may not look the best because the opponent can go to the left of it and block it from that strongly connected hex group. I would then take (B) because it is still a strong move because having a value of 3 instead of 2 means it takes the opponent 3 turns to block it from connecting.
- **Strong moves that flow with the board short ways rather than long ways are more valuable.**

#### Get Strong Moves Implementation

> "Stronger than Yesterday" - Rock Lee

Given a board state the function should return all of the moves that are strong.

##### Strong Move Tests

Simple cases

- empty board
- Single hex, simple
- Multiple single hexes
- one group of hexes
- multiple group of hexes
- Bunch of single hexes
- Bunch of groups of hexes

### Mid Game move

Mid game is the only important part for agent smart. Early game hardly exists, late game is already won. So yeah, the game plan has a few steps which is probably the entire pick a move loop.

1. **Get best path**. Classic but necessary, but in this case we care about the connections.
1. **Check connections**. Need a func for this. Get the [weak connections](/wiki/Glossary#weakly-connected) and [strong connections](/wiki/Glossary.md#strongly-connected). This agent should only make strong moves or [connection moves](/wiki/Glossary.md#connections) so there should only be one weak connection at a time due to the opponent trying to break our strong connection.
    - Fill in weak connections. Our entire game plan is based on this principle of fixing weak connections.
    - If the cost of the path is equal to the number of strong connections. We "won". Need to turn the strong connections into connections. Doesn't really matter the order.
    - At this point we are still in mid game but we have a list of strong moves which is a list of moves that we shouldn't make.
1. Get all of the strong moves.
    - Need to favour moves that lower the overall cost of the best path.
    - Moves that don't improve the cost should get checked again. These should at least be able to be used to keep the same cost. With nature of strong moves, these moves improve board control add additional options for strong moves that do improve board state. This check will filter out the strong moves in the middle of the connected spaces. In many cases these moves are still viable if the opponent blocks off the agent's initial best path.

### Get Connections

Get weak connections and get strong connections. I only care about one at a time. If there is a weak connection then make it. Compare the best path's empty hexes with the strong connections. If they are all present in the list then make one of them.

Need a way to incorporate the best path into the connections because I don't think that only the connections will give the agent enough information to make a move. When weak/strong connections happen to be on the best path, my initial idea of this function works great. But most of the strong moves are not making the best path any better. Usually strong moves are for getting board control and indirectly being able to move two spaces at once. I might be thinking of efficiency too soon. Agent Smart can be dumb for a bit. Getting the weak moves is good because there should only be one weak connection at a time if the agent/player is good. That can be done first. Getting the strong connections may not give the intended results but it is a list of moves that should not be made for any reason due to not advancing your position. I will need to come back to this for actually making strong moves. Connections can be different though. An agent must be able to understand the moves they need to make (fill weak connections) and the moves they shouldn't make (fill strong connections). I think what will happen is the agent will reach end game and not know how to close out a game until the opponent starts to fill in our strong connections.

### Smart Chain

> I think its better to do some of this implementation logic in another document and have how I want the agent to use it in here.

The [Smart Chain](./Agent-Smart/Smart-Chain.md) is a way for the agent to view it's current moves and how they connect. The agent will try and only extend from the start and end when it can and not from its middle. The chain will keep track of the [connections](/wiki/Glossary.md/#connections) and a calling [get connections](#get-connections) can be used to see if any of the connections used in the chain are weak, letting the agent know it needs to fill a bridge move.

## Review

---

Agent Smart works how I wanted it to. When uninterrupted the agent does exactly what is expected: It makes strong moves to each edge and when the chain reaches both end zones it fills in the bridge moves. Lots of useful algorithms produced with this agent and a big refactor might be needed. 

### Win percents

- over 1000 games

Opponent Agent | Agent Smart win% | Opponent win%
--|--|--
Agent A* | 80% | 20%
Agent Strong | 50% | 50%

### Agent Issues

1. #### Opponent intervention

    A big issue is when the the opponent blocks a start or end move. A one or two opponent can force the agent to "forget" about that side and never make another move on that side again. To make things worse it also forgets to make strong moves on the other end. The agent doesn't have much of a move/board evaluation to see what moves actually. Now the original game plan of the agent wasn't to care about what the opponent did but its odd that the agent plays much differently with a single move in the way.

    > probably bugs, poor algorithms, all the same

1. #### Triangle connections

    These moves are not good. If the opponent takes the middle hex then all of the other connections become weak connections. The opponent will be able to block the connection and its a waste of a move. I think this is due to the original strong move not being part of the best path (doesn't make the path shorter) so the chain doesn't use it.

    ![Triangle connection issue](/wiki/images/AgentSmartTriangleIssue.png)
