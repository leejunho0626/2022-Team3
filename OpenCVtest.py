# 이미지 출력 테스트
import cv2
print(cv2.__version__)

image = cv2.imread("C:/Users/PJS/Desktop/test123.JPG", cv2.IMREAD_ANYCOLOR)
cv2.imshow("test",image)
cv2.waitKey(0)

