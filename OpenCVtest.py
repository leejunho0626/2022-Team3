# This is a sample Python script.
import cv2
print(cv2.__version__)

image = cv2.imread("C:/Users/PJS/Desktop/test123.JPG", cv2.IMREAD_ANYCOLOR)
cv2.imshow("test",image)
cv2.waitKey(0)
cv2.destroyALLWindows()
