import pytest

@pytest.fixture(autouse=True)
def before_and_after_test(tmpdir):
  """Reset the board and pathfinder before each test"""

  # ^^^ before ^^^
  yield # run the rest
  # vvv After vvv

def test_template(tmpdir):
  assert True
