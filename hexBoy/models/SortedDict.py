from typing import Callable, List, Tuple

def _defaultGetSortValue(item):
    """Default sort value sorts by the key"""
    return item[0]

'''----------------------------------
Sorted Dict
----------------------------------'''
class SortedDict(dict):
    """Dictionary that sorts elements for pop() based on getSortValue test. 

    @param dict: dict "initial dict"
    @param getSortValue: Callable[[Tuple[any, any]], int] "What value should be used to sort the dict"
    @param reverse: bool "Which way to sort the list. True -> desc, False -> asc"
    
    Time Complexity: get O(1), set O(n), del O(n)"""

    _sortedItems: List[Tuple[any, any]] = None # sorted list of the items based on the given value
    _reverse: bool  = None  # which way to sort the list 
    _getSortValue: Callable[[Tuple[any, any]], int] = None  # which value to use to sort the list

    def __init__(self, 
        initDict: dict = None, 
        getSortValue: Callable[[Tuple[any, any]], int] = _defaultGetSortValue, 
        reverse: bool = False
    ):
        dict.__init__(self)

        self._sortedItems = []
        self._reverse = reverse
        self._getSortValue = getSortValue

        if initDict != None:
            self._appendDict(initDict)
            self._sortItems()

    # Override dict[key] = value
    def __setitem__(self, key, value):
        self._addItem(key, value)
        self._sortItems()

    # Override del(dict[key])
    def __delitem__(self, key):
        super(SortedDict, self).__delitem__(key)

        # update sortedItems with removed item
        for ind, item in enumerate(self._sortedItems):
            if item[0] == key:
                del self._sortedItems[ind]
                break

    '''---
    Private
    ---'''
    def _addItem(self, key: any, value: any):
        """Add item to dict, update sorted items"""
        if key in self:
            # Key in dict already, update entry
            super(SortedDict, self).__setitem__(key, value)

            # update sortedItems with new value
            for ind, item in enumerate(self._sortedItems):
                if item[0] == key:
                    self._sortedItems[ind] = (key, value)
                    break

        else:
            # Key not in dict, add item
            super(SortedDict, self).__setitem__(key, value)
            self._sortedItems.append((key, value))

    def _appendDict(self, D: dict):
        """Combine external dict into self, update sorted items"""
        for key in D:
            self._addItem(key, D[key])

        self._sortItems()

    def _sortItems(self):
        """Sort all of the items in the dict based on the sort value"""
        self._sortedItems.sort(key=self._getSortValue, reverse=self._reverse)

    '''---
    Public
    ---'''
    def pop(self) -> any:
        """Pop the next value out of the dict"""
        if len(self) == 0:
            return None

        else:
            key, value = self._sortedItems[0]
            del self[key]
            return value

    def popKey(self) -> any:
        """Pop the next key out of the dict"""
        if len(self) == 0:
            return None

        else:
            key, _ = self._sortedItems[0]
            del self[key]
            return key

    def popItem(self) -> tuple:
        """Pop the next (key, value) out of the dict"""
        if len(self) == 0:
            return None

        else:
            key, value = self._sortedItems[0]
            del self[key]
            return key, value

    def hasKey(self, key) -> bool:
        """Check if the dict has the key"""
        # I can use "in" but I prefer look of this
        return key in self

    def getKeys(self) -> List[any]:
        """Get the keys of the dict in order"""
        keys = []
        for i in self._sortedItems:
            keys.append(i[0])

        return keys
