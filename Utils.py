import cv2
import numpy as np

def getContours(img,cThr=[100,100],showCanny=False,minArea=1000,filter=0,draw = False):
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)# 회색조 변화
    imgBlur = cv2.GaussianBlur(imgGray,(5,5),1)# 이미지 흐림효과
    imgCanny = cv2.Canny(imgBlur,cThr[0],cThr[1])#Canny엣지 감지기 적용
    kernel =np.ones((5,5))#이미지 픽셀 작은 크기 공간 지정
    imgDial =cv2.dilate(imgCanny,kernel,iterations=3)#이미지 팽창 및 침식 적용 및 반복지정
    imgThre =cv2.erode(imgDial,kernel,iterations=2)#9~10이미지 정돈
    if showCanny:cv2.imshow('Canny',imgCanny)

    contours,hiearchy = cv2.findContours(imgThre,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    finalCountours =[]
    for i in contours:#윤곽선 영역
        area =cv2.contourArea(i)
        if area > minArea:
            peri = cv2.arcLength(i,True)#등고선
            approx =cv2.approxPolyDP(i,0.02*peri,True)#모서리 점
            bbox = cv2.boundingRect(approx)#경계 사각형
            if filter >0:
                if len(approx) == filter:
                    finalCountours.append([len(approx),area,approx,bbox,i])
                else:
                    finalCountours.append([len(approx), area, approx, bbox, i])
    finalCountours =sorted(finalCountours,key=lambda x:x[1],reverse=True)#람다를 기준으로오름차순으로 정리
    if draw:
        for con in finalCountours:
            cv2.drawContours(img,con[4],-1,(0,0,255),3)# 윤곽그리기
    return img, finalCountours

def reorder(myPoints):
    print(myPoints.shape)
    myPointsNew = np.zeros_like(myPoints)
    myPoints = myPoints.reshape((4,2))
    add = myPoints.sum(1)
    myPointsNew[0] =myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    diff = np.diff(myPoints,axis=1)
    myPointsNew[1]= myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
    return myPointsNew


def warpImg(img,points,w,h,pad=20):
   # print(points)
    points = reorder(points)
    pts1= np.float32(points)
    pts2 = np.float32([[0,0],[w,0],[0,h],[w,h]])
    martrix = cv2.getPerspectiveTransform(pts1,pts2)
    imgWarp = cv2.warpPerspective(img,martrix,(w,h))
    imgWarp =imgWarp[pad:imgWarp.shape[0]-pad,pad:imgWarp.shape[1]-pad]

    return imgWarp

def findDis(pts1,pts2):
    return ((pts2[0]-pts1[0])**2+(pts2[1]-pts1[1])**2)**0.5