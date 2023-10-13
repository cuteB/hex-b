# Smart Chain

> Because this is the time to do this

## I'm Thinkin Chains

So I got agent smart to pick the best moves. The problem is it it doesn't know how they work. Thats where the chain comes in.

![Chain with bonus points hex](/wiki/zImages/TheChain.png)

### Bonus Points

There needs to be taking each hex. How else would you pick them. There will need to be two bonus points to each hex.The first, for both players, will give hexes closer to the center more value. Next one for each player, Closer to their side is better. Leave the top and bottom at zero because they don't matter until they matter.

### Chain value

Kinda obvious thinking back. The whole game is about making a path but the smartest make chains. Chains only care about extending their length. Longer chains get to the end better. Ends gotta know when they are touching the end zone. Obviously fix weak connections but that is ezpz.  

## Smart Chain Object

Need this to be its own object. Going to be a simple linked list, defined start and end nodes that can be used to find the shortest distance to each of the ends. A sorted dict instead of the linked list because it is the goat. A list of the connections that are used to join the list. A simple `GetConnections()` call to get the weak connections to fill them in, although that is probably agent side.

### Get Chain

First thing that I need to test is a simple get function that takes in a board and returns a link. Will probably need to find the multiple chains but for now I will assume the agent is only working with a single chain. I want to have the chain as its own object but be able to initialize it with a board and a player. Probably an initialize for the player and then a function that takes in a board and builds the chain with the board.

The initialization should also include the board because I'll need the functions to grab the adjacent hexes and such.
