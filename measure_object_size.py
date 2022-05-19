import cv2
import firebase_admin
from object_detector import *
from object_size_check import *
import numpy as np
import time
import utils
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


def playVideo(route, user):
    checkStart(10.123, 13.123, user)
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

        sizecheck = object_size_check()

        # contours = detector.detect_objects(frame)  # 오츠의 기법 ?

        contours = utils.getContours(frame)  # 캐니에지 기법
        #
        cv2.drawContours(frame, contours, -1, (255, 255, 0), 3)

        for cnt in contours:
            scale = 2.80
            sizecheck_ = sizecheck.size_check(roundlist, roundcnt)
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
            if sizecheck_ == False:
                print("다른 객체 인식")
                print(sizecheck.calculat_size(roundlist))  # db
                print(sizecheck.calculat_size(matchlist))



            roundcnt += 1

        cv2.imshow("Image", frame)

        # Draw objects boundaries

    capture.release()
    cv2.destroyAllWindows()

def checkStart(round, area, id):
    doc_ref = database.collection(id).document("test")
    doc_ref.set({
        u'round': round,  # 배열[number]하면 배열[1]부터 시작하기 때문에 배열[0]부터 하기위해서 -1을 함.
        u'area': area,
        u'user': id

    })