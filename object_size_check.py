import cv2


class object_size_check():
    def __init__(self):
        pass

    def size_check(self, list_, cnt):
        if cnt < 19 or cnt % 10 + 1 != 10 : return True # 타 객체 측정시 true 값 리턴
        i = 0
        addlist1 = 0
        addlist2 = 0
        while i < 10 :
            if (cnt - 19 + i) < len(list_) :
                addlist1 = addlist1 + list_[cnt - 19 + i]
                addlist2 = addlist2 + list_[cnt - 10 + i]
                i += 1




        addlist1 = abs(addlist1 - addlist2)

        if addlist1 < 30 : return True
        else: return False         # 픽셀값의 차이가 15000이상 난다면 ?




    def calculat_size(self, list_): # 평균 값 측정


        return sum(list_) / len(list_)



