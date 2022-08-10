import sys
from hexBoy.hex.HexGame import Hex_Play
from hexBoy.AI.GetAgent import GetAgent

"""
I'll put ideas here
- Tests, do them. I wanna tryout the TTD
- Command line args to make easy to play games
- Push to GitHub more to learn make the history pretty.
"""

""" Main Function """
def main() -> None:
    agentA = GetAgent(1)
    agentB = GetAgent(1)
    showEndGame = False
    showDisplay = False
    numGames = 1
    showPrint = True

    opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
    args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

    if (len(opts) == 1 and opts[0] == "--help"): 
        printHelp()
        return

    argNum = 0 # what opt the arg is for
    for i in range(len(opts)):

        # -b <agent>, put something for a player
        if (opts[i] == "-b"):
            if (args[argNum].isnumeric()):
                agentA = GetAgent(int(args[argNum]))
            else:
                agentA = None
                showDisplay = True
            argNum += 1

        # -r <agent>
        elif (opts[i] == "-r"):
            if (args[argNum].isnumeric()):
                agentB = GetAgent(int(args[argNum]))
            else:
                agentB = None
                showDisplay = True
            argNum += 1

        # -d, for a display (auto on for players)
        elif (opts[i] == "-d"):
            showDisplay = True
        # -e, keep board on after game
        elif (opts[i] == "-e"):
            showEndGame = True
        # -n, number of games
        elif (opts[i] == "-n"):
            numGames = int(args[argNum])
            argNum += 1
        # -p, disable print
        elif (opts[i] == "-p"):
            showPrint = False

    Hex_Play(
        agentA,
        agentB,
        showEndGame,
        showDisplay,
        numGames,
        showPrint,
    )

def printHelp() -> None:
    print("So you want help.")
    print("Maybe Later")
    print("TODO") # TODO

#-------------------------------------------
#   start
#-------------------------------------------
if __name__ == "__main__":
  main()
