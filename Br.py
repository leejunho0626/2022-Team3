import numpy as np
import cv2

cap = cv2.VideoCapture(0)
#화면 크기 조절
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
brightness = 50


trackbars = np.uint8(np.full((1070, 1270, 3), 255))#트랙바 크기조절
cv2.imshow('frame', trackbars)

def brightness_change(x):
    global brightness
    brightness = x

cv2.createTrackbar('Brightness', 'frame', 0, 50, brightness_change)#트랙바 범위조절

while True:
    ret, frame = cap.read()


    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)#RGB를 HSV(색상 명도 채도)로 변경
    h, s, v = cv2.split(hsv)#각각의 영역으로 분리

    brightness_adjuster = int((brightness) / 25*25 )#밝기 영역 조절


    v_int16 = np.int16(v) + brightness_adjuster #명도조절 함수
    v_int16[v_int16 > 255] = 255
    v_int16[v_int16 < 0] = 0


    v = np.uint8(v_int16)

    final_hsv = cv2.merge((h, s, v))#HSV합치기

    image = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

    cv2.imshow('frame', image)

    if cv2.waitKey(1) == ord('q'):
        break

    if cv2.waitKey(1) == ord('p'):
        # pause기능 다른키 누르면 다시 작동
        cv2.waitKey(-1)

cap.release()
cv2.destroyAllWindows()