from hexBoy.AI.HexAgent import HexAgent

'''----------------------------------
Random Agent
----------------------------------'''
class AgentRand(HexAgent):
  """Make random moves. Rarely the best"""
  def __init__(self):
    HexAgent.__init__(self, "Agent_Rand")
 
  def getAgentMove(self):
    return self._randomMove()
