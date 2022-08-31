from hexBoy.AI.agents.AgentAStar import AgentAStar
from hexBoy.AI.agents.AgentRand import AgentRand
from hexBoy.AI.agents.AgentStrong import AgentStrong
from hexBoy.AI.agents.AgentRL import AgentRL
from hexBoy.AI.agents.AgentSmart import AgentSmart

# TODO this vvv
# TODO Change this into plugin architecture.
# - Looks cool

# TODO add None agent so player can have name
# TODO Add in a help string func that Main can call to populate the help message with what each agent number is

# Easy way to get an agent
def GetAgent(agentDifficulty=0):
    # TODO description with each agent to number
    # Random (default)
    if agentDifficulty == 0:
        return AgentRand()
    # AStar
    elif agentDifficulty == 1:
        return AgentAStar()

    # Strong
    elif agentDifficulty == 2:
        return AgentStrong()

    # RL
    elif agentDifficulty == 3:
        return AgentRL()

    # Smart
    elif agentDifficulty == 4:
        return AgentSmart()

    # just put in human
    else:
        return None # TODO make AgentHuman() that is a human player. Add in name basically it
