from hexBoy.hex.HexGame import HexGame_Play
from hexBoy.AI.GetAgent import GetAgent

def main():
  a = GetAgent(1)
  b = GetAgent(3)

  HexGame_Play(
    agentA = a,
    agentB = b,
    showEndGame = False,
    showDisplay = True,
    numGames = 1000
  )

#-------------------------------------------
#   start
#-------------------------------------------
if __name__ == "__main__":
  main()
