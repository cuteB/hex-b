from hexBoy.AI.agents.AgentAStar import AgentAStar
from hexBoy.AI.agents.AgentRand import AgentRand
from hexBoy.AI.agents.AgentStrong import AgentStrong
from hexBoy.AI.agents.AgentRL import AgentRL
from hexBoy.AI.agents.AgentSmart import AgentSmart

# TODO Change this into plugin architecture.
# - Looks cool

# Easy way to get an agent
def GetAgent(agentDifficulty=0):
  # Random (default)
  if (agentDifficulty == 0):
    return AgentRand()
  # AStar
  elif (agentDifficulty == 1):
    return AgentAStar()

  # Strong
  elif (agentDifficulty == 2):
    return AgentStrong()

  # RL
  elif (agentDifficulty == 3):
    return AgentRL()

  # Smart
  elif (agentDifficulty == 4):
    return AgentSmart()

  # just put in human
  else:
    return None
