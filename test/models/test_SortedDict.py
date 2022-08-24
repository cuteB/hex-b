import pytest
from hexBoy.models.SortedDict import SortedDict

@pytest.fixture(autouse=True)
def before_and_after_test(tmpdir):
    """Reset the board and pathfinder before each test"""
    tmpdir.dict = SortedDict()

    # ^^^ before ^^^
    yield  # run the rest
    # vvv After vvv


def test_CreateAndPopItems(tmpdir):
    """Dict should allow set, pop and check if it has a key"""
    key = 0
    item = 0
    tmpdir.dict[key] = item

    assert tmpdir.dict.hasKey(key)

    dictItem = tmpdir.dict.popItem()
    assert dictItem == (key, item)

    assert not tmpdir.dict.hasKey(key)

    dictItem = tmpdir.dict.popItem()
    assert dictItem == None


def test_AppendDict(tmpdir):
    """Should be able create with an existing dict and SortedDict"""
    putMeInCoach = {
        1: 1,
        2: 2,
        3: 3,
    }

    tmpdir.dict = SortedDict(dict=putMeInCoach)
    assert tmpdir.dict.hasKey(1)
    assert tmpdir.dict.hasKey(2)
    assert tmpdir.dict.hasKey(3)

    sd = SortedDict(dict=putMeInCoach)
    tmpdir.dict = SortedDict(dict=sd.getDict())
    assert tmpdir.dict.hasKey(1)
    assert tmpdir.dict.hasKey(2)
    assert tmpdir.dict.hasKey(3)



def test_SortItemsInDict(tmpdir):
    """Should default sort items by their key"""
    tmpdir.dict[1] = 1
    tmpdir.dict[0] = 0
    tmpdir.dict[2] = 2

    assert tmpdir.dict.popItem()[1] == 0
    assert tmpdir.dict.popItem()[1] == 1
    assert tmpdir.dict.popItem()[1] == 2


def test_CustomSortFunc(tmpdir):
    """Use custom sort fuction to change order of popped items"""

    def sortFunc(item):
        if item[1] == 2:
            return 0
        else:
            return item[1] + 10

    tmpdir.dict = SortedDict(getSortValue=sortFunc)
    tmpdir.dict[1] = 1
    tmpdir.dict[0] = 0
    tmpdir.dict[2] = 2

    assert tmpdir.dict.popItem()[1] == 2
    assert tmpdir.dict.popItem()[1] == 0
    assert tmpdir.dict.popItem()[1] == 1


def test_DeleteItemInDict(tmpdir):
    """Delete an item in the dict"""
    tmpdir.dict[0] = 0
    del tmpdir.dict[0]
    assert not tmpdir.dict.hasKey(0)


def test_UpdateItem(tmpdir):
    """Update an item and check it, make sure it stays in sorted order"""
    tmpdir.dict[0] = 0
    assert tmpdir.dict[0] == 0

    tmpdir.dict[0] = 15
    assert tmpdir.dict[0] == 15


def test_UpdateItemResort(tmpdir):
    """Update an item and check that it got sorted into its proper spot"""

    def sortFunc(item):
        return item[1]

    tmpdir.dict = SortedDict(getSortValue=sortFunc)
    tmpdir.dict[0] = 0
    tmpdir.dict[1] = 1
    tmpdir.dict[0] = 15

    assert tmpdir.dict.popItem()[1] == 1

def test_GetKeys(tmpdir):
    """Get Keys from dict"""

    tmpdir.dict[0] = 0
    tmpdir.dict[1] = 1
    tmpdir.dict[2] = 2

    expected = [0,1,2]
    actual = tmpdir.dict.getKeys()
    assert actual == expected

def test_GetSortedKeys(tmpdir):
    """Get Keys from dict that should be sorted"""

    def sortFunc(item):
        return item[1]

    tmpdir.dict = SortedDict(getSortValue=sortFunc)
    tmpdir.dict[0] = 2
    tmpdir.dict[1] = 1
    tmpdir.dict[2] = 0

    expected = [2,1,0]
    actual = tmpdir.dict.getKeys()
    assert actual == expected

def test_GetSortedKeysSameValue(tmpdir):
    """Get Keys from dict that are sorted but same value so same as input"""

    def sortFunc(item):
        return item[1]

    tmpdir.dict = SortedDict(getSortValue=sortFunc)
    tmpdir.dict[0] = 0
    tmpdir.dict[1] = 0
    tmpdir.dict[2] = 0

    expected = [0,1,2]
    actual = tmpdir.dict.getKeys()
    assert actual == expected

