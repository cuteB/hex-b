from hexGame.AI.agents.AgentAStar import AgentAStar
from hexGame.AI.agents.AgentRand import AgentRand
from hexGame.AI.agents.AgentStrong import AgentStrong
from hexGame.AI.agents.AgentRL import AgentRL


# Easy way to get an agent
def GetAgent(agentDifficulty=0):

  # AStar
  if (agentDifficulty == 1):
    return AgentAStar()

  # Strong
  elif (agentDifficulty == 2):
    return AgentStrong()

  # RL
  elif (agentDifficulty == 3):
    return AgentRL()

  # Random (default)
  else:
    return AgentRand()
