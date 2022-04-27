import cv2
from object_detector import *
from object_size_check import *
import numpy as np
import time
import utils


# Load Aruco detector


# Load Object Detector

# Load Image
target = cv2.imread("mouse.png") #매칭 대상
capture = cv2.VideoCapture(1)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 420)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 594)
i=0
roundlist = []
roundcnt = 0
matchlist = []


target_detector = HomogeneousBgDetector()
target_contours = target_detector.detect_objects(target)

while cv2.waitKey(33) < 0 :

    ret, frame = capture.read()
    detector = HomogeneousBgDetector()
    cv2.imshow("Image1", frame)
    sizecheck = object_size_check()


    contours = detector.detect_objects(frame)

    #
    cv2.drawContours(frame, contours, -1, (255,255,0), 3)


    for cnt in contours:
        scale = 2.80
        sizecheck_ = sizecheck.size_check(roundlist, roundcnt)
        length = cv2.arcLength(cnt, closed=True)/scale
        print("윤곽선의 총 길이", length)
        matchpoint = cv2.matchShapes(target_contours[0], cnt, cv2.CONTOURS_MATCH_I2, 0.0)
        print("매칭 점수", matchpoint)
        rect = cv2.minAreaRect(cnt)  # 이걸 수정
        (x, y), (w, h), angle = rect  # x, y 센터값 w, h 폭 길이, angle 기울기
        cv2.putText(frame, "round {} cm".format(round(length, 1)), (int(x+70), int(y - 30)),
                    cv2.FONT_HERSHEY_PLAIN, 1, (100, 200, 0), 2)
        cv2.putText(frame, "matchpoint {} ".format(round(matchpoint, 4)), (int(x+70), int(y + 30)),
                    cv2.FONT_HERSHEY_PLAIN, 1, (100, 200, 0), 2)
        roundlist.append(length)
        matchlist.append(matchpoint)
        if sizecheck_ == False : print("다른 객체 인식")




        roundcnt += 1

    cv2.imshow("Image", frame)


    # Draw objects boundaries
'''    for cnt in contours:
        # Get rect
        rect = cv2.minAreaRect(cnt)    # 이걸 수정
        (x, y), (w, h), angle = rect  # x, y 센터값 w, h 폭 길이, angle 기울기

        cv2.circle(frame, (int (x), int (y)), 5, (0,0,255), -1)

        box = cv2.boxPoints(rect)   # 꼭지점 좌표 사용
        box = np.int0(box) # 좌표가 float 형으로 리턴됨으로 int 형으로 변환

        cv2.polylines(frame, [box], True, (255, 0, 0), 2)
        cv2.putText(frame, "Width {} cm".format(round(w/2.62, 1)), (int(x), int(y - 30)),
                    cv2.FONT_HERSHEY_PLAIN, 1, (100, 200, 0), 2)
        cv2.putText(frame, "Height {} cm".format(round(h/2.62, 1)), (int(x), int(y + 30)),
                    cv2.FONT_HERSHEY_PLAIN, 1, (100, 200, 0), 2)


    cv2.imshow("Image", frame)
'''








capture.release()
cv2.destroyAllWindows()