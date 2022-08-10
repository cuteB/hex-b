import sys
from hexBoy.hex.HexGame import HexGame_Play
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

  argNum = 0 # what opt the arg is for
  for i in range(len(opts)):
    if (opts[i] == "-b"):
      if (args[argNum].isnumeric()):
        agentA = GetAgent(int(args[argNum]))
      else:
        agentA = None
        showDisplay = True

      argNum += 1
    elif (opts[i] == "-r"):
      if (args[argNum].isnumeric()):
        agentB = GetAgent(int(args[argNum]))
      else:
        agentB = None
        showDisplay = True

      argNum += 1
    elif (opts[i] == "-d"):
      showDisplay = True
    elif (opts[i] == "-e"):
      showEndGame = True
    elif (opts[i] == "-n"):
      numGames = int(args[argNum])
      argNum += 1
    elif (opts[i] == "-p"):
      showPrint = False



  HexGame_Play(
    agentA,
    agentB,
    showEndGame,
    showDisplay,
    numGames,
    showPrint,
  )

#-------------------------------------------
#   start
#-------------------------------------------
if __name__ == "__main__":
  main()
