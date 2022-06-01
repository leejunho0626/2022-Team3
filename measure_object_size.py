from datetime import datetime

import cv2
import rulebase
import firebase_admin

from object_detector import *
from object_size_check import *
import numpy as np
import utils
from rulebase import *

from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import auth
from firebase_admin import firestore

# Firebase database 인증 및 앱 초기화(Realtime Database, Firestore Database)
cred = credentials.Certificate('key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://teamproject-642cf-default-rtdb.firebaseio.com/'
    # 'databaseURL' : '데이터 베이스 url'
})  # Realtime Database
database = firestore.client()  # Firestore Database

brightness = 50
trackbars = np.uint8(np.full((410, 594, 3), 255))  # 트랙바 크기조절

def brightness_change(x):
    global brightness
    brightness = x

def playVideo(route, user, r_size, r_area):
    cnt_ = 1
    capture = cv2.VideoCapture(0)

    cv2.imshow('frame', trackbars)

    cv2.createTrackbar('Brightness', 'frame', 0, 50, brightness_change)  # 트랙바 범위조절



    target = cv2.imread(route)  # 매칭 대상
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 420)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 594)


    i = 0
    roundlist = []
    roundcnt = 0
    matchlist = []
    arealist = []

    target_detector = HomogeneousBgDetector()
    target_contours = target_detector.detect_objects(target)

    scalecheck_ = 1

    while cv2.waitKey() != 27:
        image2 = np.zeros((500, 500, 3), np.uint8)
        if cv2.waitKey() == ord('s'):
            print("stop")
            cv2.putText(image2, "Stop!".format(round(length, 1)), (int(x + 70), int(y - 30)),
                        cv2.FONT_HERSHEY_PLAIN, 1, (100, 200, 0), 2)

        elif cv2.waitKey() == ord('p'):
            print("play")


        ret, frame = capture.read()
        # detector = HomogeneousBgDetector()
        sizecheck = object_size_check()


        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # RGB를 HSV(색상 명도 채도)로 변경
        h, s, v = cv2.split(hsv)  # 각각의 영역으로 분리
        brightness_adjuster = int((brightness) / 25 * 25)  # 밝기 영역 조절

        v_int16 = np.int16(v) + brightness_adjuster  # 명도조절 함수
        v_int16[v_int16 > 255] = 255
        v_int16[v_int16 < 0] = 0

        v = np.uint8(v_int16)

        final_hsv = cv2.merge((h, s, v))  # HSV합치기

        image = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

        # contours = detector.detect_objects(frame)  # 오츠의 기법 ?

        contours = utils.getContours(image)  # 캐니에지 기법
        #
        cv2.drawContours(image, contours, -1, (255, 255, 0), 3)

        for cnt in contours:
            sizescale = 8.2156
            areascale = 600.269
            #if scalecheck_ == 1 :
            #    scalecheck_ = 0;
            #    length = cv2.arcLength(cnt, closed=True)
            #    area = cv2.contourArea(cnt, oriented=None)
            #    sizescale, areascale = scale_chcek(length, 5, area, 25)


            sizecheck_ = sizecheck.size_check(roundlist, roundcnt)

            length = cv2.arcLength(cnt, closed=True) / sizescale
            # print("윤곽선의 총 길이", length)
            matchpoint = cv2.matchShapes(target_contours[0], cnt, cv2.CONTOURS_MATCH_I3, 0.0)
            # print("매칭 점수", matchpoint)
            area = cv2.contourArea(cnt, oriented=None) / areascale

            rect = cv2.minAreaRect(cnt)  # 이걸 수정
            (x, y), (w, h), angle = rect  # x, y 센터값 w, h 폭 길이, angle 기울기
            cv2.putText(image, "round {} mm".format(round(length, 1)), (int(x + 70), int(y - 30)),
                        cv2.FONT_HERSHEY_PLAIN, 1, (100, 200, 0), 2)
            cv2.putText(image, "matchpoint {} ".format(round(matchpoint, 4)), (int(x + 70), int(y + 30)),
                        cv2.FONT_HERSHEY_PLAIN, 1, (100, 200, 0), 2)
            cv2.putText(image, "area {} mm x mm ".format(round(area, 1)), (int(x + 70), int(y + 15)),
                        cv2.FONT_HERSHEY_PLAIN, 1, (100, 200, 0), 2)


            roundlist.append(length)
            matchlist.append(matchpoint)
            arealist.append(area)

            if len(roundlist) > 30 :
                if sizecheck_ == False:
                    print("다른 객체 인식")

                    #rsz_, mtz_, arz_ = rulebase.del_arr(200, roundlist, matchlist, arealist)

                    rsz = sizecheck.calculat_size(roundlist)

                    mtz = sizecheck.calculat_size(matchlist)

                    arz = sizecheck.calculat_size(arealist)


                    print(rsz, mtz, arz)

                    now = datetime.now()  # 시간
                    print(now)
                    print(str(rulebase.rule_algorithm(200, rsz, mtz, 250, arz)))
                    doc_ref = database.collection(user).document(str(cnt_))
                    doc_ref.set({
                        u'round': str(rsz),
                        u'area': str(arz),
                        u'user': user,
                        u'result': str(rulebase.rule_algorithm(200, rsz, mtz, 250, arz)),
                        u'time': str(now.strftime('%Y-%m-%d %H:%M:%S'))
                    })

                    roundlist = []
                    matchlist = []
                    arealist = []
                    roundcnt = -1
                    cnt_ += 1


                continue





            roundcnt += 1
        cv2.imshow("frame", image)

        # Draw objects boundaries

    capture.release()
    cv2.destroyAllWindows()
