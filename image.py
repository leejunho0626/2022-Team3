import cv2
import sys

img = cv2.imread('real.png')

if img is None:
    print('이미지가 없음')
    sys.exit()

cv2.namedWindow('image')
cv2.imshow('image',img)
cv2.waitKey()

