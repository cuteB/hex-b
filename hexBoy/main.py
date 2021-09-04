from hexGame.HexGame import HexGame_main
from hexGame.AI.GetAgent import GetAgent

def main():
  a = GetAgent(2)
  b = GetAgent(1)

  HexGame_main(
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
