from hexBoy.AI.agents.AgentAStar import AgentAStar
from hexBoy.AI.agents.AgentRand import AgentRand
from hexBoy.AI.agents.AgentRL import AgentRL
from hexBoy.AI.agents.AgentSmart import AgentSmart
from hexBoy.AI.agents.AgentStrong import AgentStrong
from hexBoy.AI.HexAgent import HexAgent

# COMEBACK Change this into plugin architecture.
# - Looks cool
# - add None agent so player can have name

# Easy way to get an agent
def GetAgent(agentDifficulty=0) -> HexAgent:
    """Get an agent given an Id"""
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
        return None 

def PrintAgentHelp() -> None:
    """Print the id to Agent help message"""
    print("Agent List")
    print("0 \tAgent Random")
    print("1 \tAgent AStar")
    print("2 \tAgent Strong")
    print("3 \tAgent RL")
    print("4 \tAgent Smart")
    print()
