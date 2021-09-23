"""Dict actually working well. Maybe a bit of love to make it more readable"""

'''
-----------------------------------------------
Hexagon shape for board
-----------------------------------------------
'''
class SortedDict(dict):
  _dictionary   = None  # the dict
  _sortedItems  = None  # sorted list of the items based on the given value
  _reverse      = None  # which way to sort the list
  _getSortValue = None  # which value to use to sort the list

  def __init__(self, dict = None, getSortValue = None, reverse = False):
    dict.__init__(self)

    self._sortedItems = []
    self._reverse = reverse

    # Set the getSortValue function
    if (getSortValue == None):
      self._getSortValue = self._defaultGetSortValue
    else:
      self._getSortValue = getSortValue

    # Init the dict
    if (dict == None):
      self._dictionary = {}
    else:
      self._dictionary = dict
      self._appendDict(dict)
      self._sortItems()

  '''
  ------------------
  Overide dict functions
  ------------------
  '''
  # dict[key] = value
  def __setitem__(self, key, value):
    self._addItem(key, value)
    self._sortItems()

  # del(dict[key])
  def __delitem__(self, key):
    super(SortedDict, self).__delitem__(key)

    # update sortedItems with removed item
    for ind, item in enumerate(self._sortedItems):
      if item[0] == key:
        del(self._sortedItems[ind])
        break

  '''
  ------------------
  Private functions
  ------------------
  '''
  # Add item to dict, update sorted items
  def _addItem(self, key, value):
    if (key in self):
      # Key in dict already, update entry
      super(SortedDict, self).__setitem__(key, value)

      # update sortedItems with new value
      for ind, item in enumerate(self._sortedItems):
        if item[0] == key:
          self._sortedItems[ind] = (key,value)
          break

    else:
      # Key not in dict, add item
      super(SortedDict, self).__setitem__(key, value)
      self._sortedItems.append((key, value))

  # Combine external dict into self, update sorted items
  def _appendDict(self, dict):
    for key in dict:
      print(key)
      self._addItem(key, dict[key])

    self._sortItems()

  # Sort all of the items in the dict based on the sort value
  def _sortItems(self):
    self._sortedItems.sort(key=self._getSortValue, reverse=self._reverse)

  # Grab the value that will be used to sort the dict items
  def _defaultGetSortValue(self, item):
    return item[0] # Just use the key if no other getValue is provided

  '''
  ------------------
  Public functions
  ------------------
  '''
  # pop off the lowest item (first item in sortedItems)
  def popItem(self):
    if (len(self) == 0):
      return None

    else:
      key, value = self._sortedItems[0]
      del(self[key])
      return key, value

  def hasKey(self, key):
    return (key in self)

  def getDict(self):
    return self._dictionary
