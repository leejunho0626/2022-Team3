import cv2


class object_size_check():
    def __init__(self):
        pass

    def size_check(self, list_, cnt):  # 10개씩 막 더해서 손이 들어왔는지체크 return 값은 불값
        if cnt < 19 or cnt % 10 + 1 != 10 : return True

        # list_[cnt-19] ~ list_[cnt-10]       list[cnt-9] ~ list[cnt]
        i = 0
        addlist1 = 0
        addlist2 = 0
        while i < 10 :
            addlist1 = addlist1 + list_[cnt -19 + i]
            addlist2 = addlist2 + list_[cnt - 10 + i]
            i += 1


        addlist1 = abs(addlist1 - addlist2)

        if addlist1 < 300 : return True
        else: return False         # 픽셀값의 차이가 15000이상 난다면 ?




    def calculat_size(self, list_):
        count = []
        i = 0
        cnt = 0

        while i < len(list_):
            count.append(round(list_[i]))
            i += 1

        i = 0
        num = 0
        temp = 0
        tmp = 0

        while i < len(count):
            num = count[i]
            j = 0
            while j < len(count):
                if num == count[j]:
                    cnt += 1
                j += 1
            if temp < cnt:
                tmp = num
                temp = cnt
            cnt = 0

            i += 1

        i = 0
        cnt = 0
        add = 0
        while i < len(list_):
            if tmp - 1.5 < list_[i] < tmp + 1.5:
                add += list_[i]
                cnt += 1

            i += 1

        return add / cnt

        #cnt 39라 가정
        #cnt 29~39 값 cnt 19~29 값 비교


    #리턴값 참 거짓 값


    #def 일정 초과 값이나 사이즈 값에 미치지 못하는 값 제거

    #def 평균값 추출 여기서 matchpoint 평균값도 해주면 될듯



