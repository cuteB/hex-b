from hexBoy.hex.HexGame import HexGame_Play
from hexBoy.AI.GetAgent import GetAgent

"""
I'll put ideas here
- Tests, do them. I wanna tryout the TTD
- Command line args to make easy to play games
- Push to GitHub more to learn make the history pretty.
"""


def main() -> None:
  """ Main Function """
  a = GetAgent(4)
  b = GetAgent(1)

  HexGame_Play(
    agentA = a,
    agentB = b,
    showEndGame = False,
    showDisplay = True,
    numGames = 10
  )

#-------------------------------------------
#   start
#-------------------------------------------
if __name__ == "__main__":
  main()
