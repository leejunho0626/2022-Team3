import cv2


class HomogeneousBgDetector():
    def __init__(self):
        pass

    def detect_objects(self, frame): #오츠의 기법

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # 그레이 스케일 변경
        mask = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 19, 5) # 마스크 적용 후 잡티 제거

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)    #윤곽잡기

        objects_contours = []

        for cnt in contours:
            area = cv2.contourArea(cnt) # area값 측정 후
            if area > 500: # 면적이 500이 넘어갈경우 contours 리스트에 저장
                objects_contours.append(cnt)

        return objects_contours
