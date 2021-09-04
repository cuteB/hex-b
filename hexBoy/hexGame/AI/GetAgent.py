from hexGame.AI.agents.AgentAStar import AgentAStar
from hexGame.AI.agents.AgentRand import AgentRand
from hexGame.AI.agents.AgentStrong import AgentStrong

# Easy way to get an agent
def GetAgent(agentDifficulty=0):

  # AStar
  if (agentDifficulty == 1):
    return AgentAStar()

  # Strong
  elif (agentDifficulty == 2):
    return AgentStrong()

  # Random (default)
  else:
    return AgentRand()
