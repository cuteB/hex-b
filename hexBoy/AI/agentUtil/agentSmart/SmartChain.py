from hexBoy.models.SortedDict import SortedDict

'''----------------------------------
Smart Chain
----------------------------------'''
# > By mister Reed

class SmartChain:
    nodeDict: SortedDict = None

    def __init__(self):
        self.nodeDict = SortedDict()
