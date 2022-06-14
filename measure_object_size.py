import tkinter.messagebox
from datetime import datetime
from tkinter import *
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
import re


# Firebase database 인증 및 앱 초기화(Realtime Database, Firestore Database)
cred = credentials.Certificate('C:/Users/dongl/PycharmProjects/pythonProject1/key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://teamproject-642cf-default-rtdb.firebaseio.com/'
    # 'databaseURL' : '데이터 베이스 url'
})  # Realtime Database
database = firestore.client()  # Firestore Database

brightness = 50
trackbars = np.uint8(np.full((410, 594, 3), 255))  # 트랙바 크기조절

def brightness_change(x): #밝기조절
    global brightness
    brightness = x



def playVideo(route, user, r_size, r_area): # 불량품 측정 //  route : 유사도 판별 사진 경로, user : database user
                                            # r_size : 측정하려는 물체의 둘레 값,  r_area : 측정하려는 물체의 넓이 값.

    capture = cv2.VideoCapture(1)

    users_ref = database.collection(u'scale')
    docs = users_ref.stream()
    strtmp = ""
    for doc in docs:
        strtmp = str(doc.to_dict())


    tmp_str2 = strtmp.split("'")

    sizescale = float(tmp_str2[3]) #둘레 스케일 값 파싱
                                    
    areascale = float(tmp_str2[7]) #넓이 스케일 값 파싱

    if sizescale > areascale : # 스케일 값이 바뀌는 오류 수정을 위해 sizescale 값이 항상 커야하니 바꿈
        tmp = sizescale
        sizescale = areascale
        areascale = tmp



    cv2.imshow('frame', trackbars)

    cv2.createTrackbar('Brightness', 'frame', 50, 50, brightness_change)  # 트랙바 범위조절

    target = cv2.imread(route)  # 매칭 대상
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 420)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 594)


    roundlist = []  # 둘레 값을 전체적으로 저장
    roundcnt = 0
    matchlist = [] # 유사도 값을 전체적으로 저장
    arealist = [] # 넓이 값을 전체적으로 저장

    target_detector = HomogeneousBgDetector()
    target_contours = target_detector.detect_objects(target) #유사도 측정을 위해 오츠의 기법을 통함.

    while cv2.waitKey(33) != ord('q') :  # q누르면 영상 종료.

        if re.sub(r'[^0-9]', '', r_size) == "": # match값이 비어있거나 숫자가 아닌 값이 입력 될 경우 오류메시지 출력
            tkinter.messagebox.showinfo("값 입력 오류", "값이 올바르지 않습니다.")
            break;
        if re.sub(r'[^0-9]', '', r_area) == "": #''
            tkinter.messagebox.showinfo("값 입력 오류", "값이 올바르지 않습니다.")
            break;

        ret, frame = capture.read()
        # detector = HomogeneousBgDetector()
        sizecheck = object_size_check()

        recheck = True


        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # RGB를 HSV(색상 명도 채도)로 변경
        h, s, v = cv2.split(hsv)  # 각각의 영역으로 분리
        brightness_adjuster = int((brightness) / 25 * 25)  # 밝기 영역 조절

        v_int16 = np.int16(v) + brightness_adjuster  # 명도조절 함수
        v_int16[v_int16 > 255] = 255
        v_int16[v_int16 < 0] = 0

        v = np.uint8(v_int16)

        final_hsv = cv2.merge((h, s, v))  # HSV합치기

        image = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

        contours = utils.getContours(image)  # 캐니에지 기법

        cv2.drawContours(image, contours, -1, (255, 255, 0), 3) #윤곽선을 표시해줌

        for cnt in contours: #길이를 표시해주고, 측정값을 저장하기위함.

            length = cv2.arcLength(cnt, closed=True) / sizescale  # 측정한 스케일 값을 기반으로 둘레 값 조정
            matchpoint = cv2.matchShapes(target_contours[0], cnt, cv2.CONTOURS_MATCH_I3, 0.0) #유사도 값 측정
            area = cv2.contourArea(cnt, oriented=None) / areascale # 측정한 스케일 값을 기반으로 면적 측정

            rect = cv2.minAreaRect(cnt) #cnt의 좌표 및 기울기 값 계산
            (x, y), (w, h), angle = rect  # x, y 센터값 w, h 폭 길이, angle 기울기
            cv2.putText(image, "round {} mm".format(round(length, 1)), (int(x + 70), int(y - 30)),
                        cv2.FONT_HERSHEY_PLAIN, 1.5, (100, 200, 0), 2)
            cv2.putText(image, "matchpoint {} ".format(round(matchpoint, 4)), (int(x + 70), int(y + 30)),
                        cv2.FONT_HERSHEY_PLAIN, 1.5, (100, 200, 0), 2)
            cv2.putText(image, "area {} mm x mm ".format(round(area, 1)), (int(x + 70), int(y)),
                        cv2.FONT_HERSHEY_PLAIN, 1.5, (100, 200, 0), 2)


            roundlist.append(length) ##roundlist 추가
            matchlist.append(matchpoint) ##''
            arealist.append(area) ##''
 
            if len(roundlist) > 100 : # 값이 100개가 넘었다면. 대략 7초 소요

                rsz = sizecheck.calculat_size(roundlist) ## 둘레 평균값

                mtz = sizecheck.calculat_size(matchlist) ## 유사도  평균값

                arz = sizecheck.calculat_size(arealist) ## 넓이 평균값

                result = str(rulebase.rule_algorithm(float(r_size), rsz, mtz, float(r_area), arz)) ## 룰베이스 알고리즘을 적용하여 불량값 판별

                msg = tkinter.messagebox.askquestion('재측정여부', '       결과 : {0}\n\n 재측정을 하시겠습니까?'.format(result))
                if msg == "no": # 불량값이 측정되었다면 밝기를 조정하여 재측정을 할 것인지 안 한다면 데이터베이스 전송

                    now = datetime.now()  # 시간
                    nowTime = now.strftime('%Y.%m.%d.%H:%M:%S')

                    doc_ref = database.collection(user).document(nowTime)
                    doc_ref.set({
                        u'round': str(round(rsz, 2)),
                        u'area': str(round(arz, 2)),
                        u'user': user,
                        u'result': str(rulebase.rule_algorithm(float(r_size), rsz, mtz, float(r_area), arz)),
                        u'time': str(now.strftime('%Y-%m-%d %H:%M:%S'))
                    })

                    roundlist = [] #리스트 초기화
                    matchlist = []
                    arealist = []
                    roundcnt = -1
                    recheck = False


                    break
                else:
                    roundlist = []
                    matchlist = []
                    arealist = []
                    roundcnt = -1
                    tkinter.messagebox.showinfo("재측정여부", "밝기 조정 및 재측정 하세요.")

            roundcnt += 1

        cv2.imshow("frame", image)
        if recheck == False:
            tkinter.messagebox.showinfo("완료", "측정이 완료되었습니다.")
            break;



    capture.release()
    cv2.destroyAllWindows()

def checkStart(round, area, id):
    doc_ref = database.collection(id).document("test")
    doc_ref.set({
        u'round': round,  # 배열[number]하면 배열[1]부터 시작하기 때문에 배열[0]부터 하기위해서 -1을 함.
        u'area': area,
        u'user': id

    })



def playscale(user): #스케일 측정
    capture = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    cv2.imshow('frame', trackbars)
    cv2.createTrackbar('Brightness', 'frame', 50, 50, brightness_change)  # 트랙바 범위조절

    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 420)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 594)
    check = True

    roundlist = []
    arealist = []


    while cv2.waitKey(33) != ord('q'):
        ret, frame = capture.read()
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
        contours = utils.getContours(image)
        cv2.drawContours(image, contours, -1, (255, 255, 0), 3)

        for cnt in contours:
            length = cv2.arcLength(cnt, closed=True)
            area = cv2.contourArea(cnt, oriented=None)


            roundlist.append(length)
            arealist.append(area)

            if len(roundlist) > 30 :
                rsz = sizecheck.calculat_size(roundlist)
                arz = sizecheck.calculat_size(arealist)

                roundlist = []
                arealist = []

                s_scale, a_scale = rulebase.scale_chcek(rsz, 200, arz, 2500) # 50mm 값의 둘레 200 넓이 2500
                doc_ref = database.collection("scale").document(user)
                doc_ref.set({
                    u'size': str(s_scale),
                    
                    u'area': str(a_scale)
                })

                check = False





        cv2.imshow("frame", image)
        if check == False:
            tkinter.messagebox.showinfo("완료", "스케일 측정이 완료되었습니다.")
            break;



    capture.release()
    cv2.destroyAllWindows()


def onlyVideo(): # 기본적 카메라를 보여줌
    capture = cv2.VideoCapture(1, cv2.CAP_DSHOW)

    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 420)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 594)


    while cv2.waitKey(33) != ord('q'):
        ret, frame = capture.read()
        cv2.imshow("frame", frame)

    capture.release()
    cv2.destroyAllWindows()
