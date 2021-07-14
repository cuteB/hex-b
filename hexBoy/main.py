import cv2
from board.hexagon import hexBoard


def main():
  print('Am hex boy')

  board = hexBoard()
  cv2.imshow('image', board)
  cv2.waitKey()


#-------------------------------------------
#   start
#-------------------------------------------
if __name__ == "__main__":
  main()
