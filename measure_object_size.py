import cv2
from object_detector import *
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Load Aruco detector


# Load Object Detector

# Load Image
#img = cv2.imread("phone_aruco_marker.jpg")
# Firebase database 인증 및 앱 초기화
cred = credentials.Certificate('key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://teamproject-642cf-default-rtdb.firebaseio.com/'
    # 'databaseURL' : '데이터 베이스 url'
})

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 420)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 594)

while cv2.waitKey(33) < 0 :

    ret, frame = capture.read()
    detector = HomogeneousBgDetector()

    contours = detector.detect_objects(frame)


    # Draw objects boundaries
    for cnt in contours:
        # Get rect
        rect = cv2.minAreaRect(cnt)
        (x, y), (w, h), angle = rect  # x, y 센터값 w, h 폭 길이, angle 기울기

        cv2.circle(frame, (int (x), int (y)), 5, (0,0,255), -1)

        box = cv2.boxPoints(rect)   # 꼭지점 좌표 사용
        box = np.int0(box) # 좌표가 float 형으로 리턴됨으로 int 형으로 변환

        cv2.polylines(frame, [box], True, (255, 0, 0), 2)
        cv2.putText(frame, "Width {} cm".format(round(w, 1)), (int(x), int(y - 30)),
                    cv2.FONT_HERSHEY_PLAIN, 1, (100, 200, 0), 2)
        cv2.putText(frame, "Height {} cm".format(round(h, 1)), (int(x), int(y + 30)),
                    cv2.FONT_HERSHEY_PLAIN, 1, (100, 200, 0), 2)
        # db 위치 지정, 기본 가장 상단을 가르킴
        i=1


        ref = db.reference('Result/제품'+str(i))  # 경로가 없으면 생성한다.
        ref.update({'가로': round(w)})
        ref.update({'세로': round(h)})
        print(round(w),round(h))




    cv2.imshow("Image", frame)

capture.release()
cv2.destroyAllWindows()