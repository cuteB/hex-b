# Hex-b

> The only reason I'm here

Hex, The game

## Quick Start Guide

```bash
$ pip install -r requirements.txt
$ python main.py
```

This will run a game between two agents and won't really show much other than some text saying who wins. 
To get some more options add the `--help` flag or checkout the [Hex Game Page](./wiki/hex.md)

## [The Game and Rules](./wiki/hex/Hex-Rules.md)

Here is an example game where Blue wins.

![Random Hex Game](/wiki/zImages/boards/RandomHexBoard.png)

This is what the hex space looks like. 
Just treat them like squares with too extra edges.

```txt
 ___
/0,0\___
\___/1,0\___
/0,1\___/2,0\___
\___/1,1\___/3,0\___
/0,2\___/2,1\___/4,0\
\___/1,2\___/3,1\___/
/0,3\___/2,2\___/4,1\
\___/1,3\___/3,2\___/
/0,4\___/2,3\___/4,2\
\___/1,4\___/3,3\___/
    \___/2,4\___/4,3\
        \___/3,4\___/
            \___/4,4\
                \___/
```

### [Game Agents](./wiki/Agents.md)

The list of agents that know how to play the game.
How do you compare?