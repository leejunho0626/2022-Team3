import cv2
import rulebase

from object_detector import *
from object_size_check import *
import numpy as np
import time
import utils
from datetime import datetime
from rulebase import *


def playVideo(route):
    target = cv2.imread(route)  # 매칭 대상
    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 420)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 594)
    i = 0
    roundlist = []
    roundcnt = 0
    matchlist = []

    target_detector = HomogeneousBgDetector()
    target_contours = target_detector.detect_objects(target)

    while cv2.waitKey(33) < 0:

        ret, frame = capture.read()
        # detector = HomogeneousBgDetector()
        cv2.imshow("Image1", frame)
        sizecheck = object_size_check()

        # contours = detector.detect_objects(frame)  # 오츠의 기법 ?

        contours = utils.getContours(frame)  # 캐니에지 기법
        #
        cv2.drawContours(frame, contours, -1, (255, 255, 0), 3)
        second_check = 0;

        for cnt in contours:
            scale = 2.80
            sizecheck_ = sizecheck.size_check(roundlist, roundcnt)
            now = datetime.now()
            second = now.second
            length = cv2.arcLength(cnt, closed=True) / scale
            # print("윤곽선의 총 길이", length)
            matchpoint = cv2.matchShapes(target_contours[0], cnt, cv2.CONTOURS_MATCH_I3, 0.0)
            # print("매칭 점수", matchpoint)
            rect = cv2.minAreaRect(cnt)  # 이걸 수정
            (x, y), (w, h), angle = rect  # x, y 센터값 w, h 폭 길이, angle 기울기
            cv2.putText(frame, "round {} cm".format(round(length, 1)), (int(x + 70), int(y - 30)),
                        cv2.FONT_HERSHEY_PLAIN, 1, (100, 200, 0), 2)
            cv2.putText(frame, "matchpoint {} ".format(round(matchpoint, 4)), (int(x + 70), int(y + 30)),
                        cv2.FONT_HERSHEY_PLAIN, 1, (100, 200, 0), 2)
            roundlist.append(length)
            matchlist.append(matchpoint)
            if len(roundlist) > 100 :
                if sizecheck_ == False:
                    print("다른 객체 인식")
                    print(sizecheck.calculat_size(roundlist))
                    print(sizecheck.calculat_size(matchlist))
                    roundlist.clear()
                    matchlist.clear()
                    #print(rulebase.rule_algorithm()) # true false값



            roundcnt += 1

        cv2.imshow("Image", frame)

        # Draw objects boundaries

    capture.release()
    cv2.destroyAllWindows()
