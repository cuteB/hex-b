import cv2
from hexGame.hexagon import hexBoard

def clickCallback(event,x,y,flags,param):
  print(x + "," + y)


def main():
  print('Am hex boy')

  board = hexBoard(11)
  cv2.setMouseCallback('image',clickCallback)
  cv2.imshow('image', board)
  cv2.waitKey(0)



#-------------------------------------------
#   start
#-------------------------------------------
if __name__ == "__main__":
  main()
