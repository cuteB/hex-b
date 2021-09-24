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
  agentA = None
  agentB = None
  showEndGame = True
  showDisplay = True
  numGames = None

  opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
  args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

  argNum = 0 # what opt the org is for
  for i in range(len(opts)):
    if (opts[i] == "-b"):
      agentA = GetAgent(int(args[argNum]))
      argNum += 1
    elif (opts[i] == "-r"):
      agentB = GetAgent(int(args[argNum]))
      argNum += 1
    elif (opts[i] == "-d"):
      showDisplay = False
    elif (opts[i] == "-e"):
      showEndGame = False
    elif (opts[i] == "-n"):
      numGames = int(args[argNum])
      argNum += 1

  a = GetAgent(1)
  b = GetAgent(3)

  HexGame_Play(
    agentA,
    agentB,
    showEndGame,
    showDisplay,
    numGames
  )

#-------------------------------------------
#   start
#-------------------------------------------
if __name__ == "__main__":
  main()
