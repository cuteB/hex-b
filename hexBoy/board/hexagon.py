import math
import numpy as np
from PIL import Image
from aggdraw import Draw, Brush, Pen
import matplotlib.pyplot as plt
from matplotlib.image import imread

def hexBoard():
  image = Image.new('RGB', (500, 800), 'white')
  draw = Draw(image)
  hexagon_generator = HexagonGenerator(40)

  boardSize = 8

  for row in range(boardSize):
    for col in range(boardSize):
      colour = getHexColour(boardSize, row, col)
      label = getHexLabel(row, col)
      hexagon = hexagon_generator(row, col)
      draw.polygon(list(hexagon), Pen('black'), Brush(colour))

  draw.flush()

  # convert to np array and return
  np_img = np.array(image)
  return np_img

# look at a given board and return the colour of the hex
def getHexColour(boardSize, row, col):
  size = boardSize - 1

  if (row == 0 and col == 0) or (row == size and col == size):
    return 'black'
  if (row == 0 or row == size):
    return 'blue'
  elif (col == 0) or (col == size):
    return 'red'
  else:
    return 'white'

def getHexLabel(row, col):
  if (row != 0 and col != 0):
    return ""

class HexagonGenerator(object):
  """Returns a hexagon generator for hexagons of the specified size"""

  def __init__(self, edge_length):
    self.edge_length = edge_length

  @property
  def col_width(self):
    return self.edge_length * 1.5

  @property
  def row_height(self):
    return math.sin(math.pi / 3) * self.edge_length

  def __call__(self, row, col):
    x = 20 + (col * self.col_width)
    y = (row * self.row_height * 2) + (col * self.row_height)
    for angle in range(0, 360, 60):
      x += math.cos(math.radians(angle)) * self.edge_length
      y += math.sin(math.radians(angle)) * self.edge_length
      yield x
      yield y
