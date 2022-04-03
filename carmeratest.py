#카메라 출력 테스트

import cv2

capture = cv2.VideoCapture(0)#카메라 장치번호
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280) #가로
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 800) #세로

while cv2.waitKey(1) != ord('q'):#q버튼 누를때 종료
    ret, frame = capture.read()#ret=카메라 상태 저장 작동시true 그렇지 않으면 false저장
    cv2.imshow("VideoFrame", frame)

capture.release()
cv2.destroyAllWindows()
