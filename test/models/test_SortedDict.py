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
        1: "a",
        2: "b",
        3: "c",
    }

    tmpdir.dict = SortedDict(initDict=putMeInCoach)
    assert tmpdir.dict.hasKey(1)
    assert tmpdir.dict.hasKey(2)
    assert tmpdir.dict.hasKey(3)

    sd = SortedDict(initDict=putMeInCoach)
    print(sd)
    print(putMeInCoach)

    tmpdir.dict = SortedDict(initDict=sd)
    print(tmpdir.dict.getKeys())
    assert tmpdir.dict.hasKey(1)
    assert tmpdir.dict.hasKey(2)
    assert tmpdir.dict.hasKey(3)

def test_SortItemsInDictWithPop(tmpdir):
    """Should default sort items by their key"""
    tmpdir.dict[2] = "b"
    tmpdir.dict[1] = "a"
    tmpdir.dict[3] = "c"

    assert tmpdir.dict.pop() == "a"
    assert tmpdir.dict.pop() == "b"
    assert tmpdir.dict.pop() == "c"

def test_SortItemsInDictWithPopItem(tmpdir):
    """Should pop key,value"""
    tmpdir.dict[2] = "b"
    tmpdir.dict[1] = "a"
    tmpdir.dict[3] = "c"

    assert tmpdir.dict.popItem() == (1, "a")
    assert tmpdir.dict.popItem() == (2, "b")
    assert tmpdir.dict.popItem() == (3, "c")

def test_SortItemsInDictWithPopKey(tmpdir):
    """Should pop key"""
    tmpdir.dict[2] = "b"
    tmpdir.dict[1] = "a"
    tmpdir.dict[3] = "c"

    assert tmpdir.dict.popKey() == 1
    assert tmpdir.dict.popKey() == 2
    assert tmpdir.dict.popKey() == 3

def test_CustomSortFunc(tmpdir):
    """Use custom sort function to change order of popped items"""

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
