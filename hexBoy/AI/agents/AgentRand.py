from hexBoy.AI.HexAgent import HexAgent
from hexBoy.hex.node.HexNode import Hex

'''----------------------------------
Random Move Agent
----------------------------------'''
class AgentRand(HexAgent):
    """Make random moves. Rarely the best"""

    def __init__(self):
        HexAgent.__init__(self, "Agent_Rand")

    # Override
    def getAgentMove(self) -> Hex:
        return self._randomMove()
