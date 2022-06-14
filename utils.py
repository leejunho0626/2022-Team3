import cv2
import numpy as np

def getContours(frame,cThr=[10,70]): #케니에지 기법
    imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #회색 화면으로 적용
    imgBlur = cv2.GaussianBlur(imgGray, (5,5), 1) #가우시안 필터링 적용 후 잡티 제거
    imgCanny = cv2.Canny(imgBlur,cThr[0], cThr[1]) #기울기 값 기반으로 케니에지 기법 적용
    kernel = np.ones((5,5))
    imgDial = cv2.dilate(imgCanny,kernel, iterations=3)
    imgThre = cv2.erode(imgDial, kernel, iterations=2)
    contours, _ = cv2.findContours(imgThre, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # contours값 리스트

    return contours

