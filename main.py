import uuid

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import auth
from firebase_admin import firestore
import random
from datetime import datetime
from tkinter import *
import tkinter.messagebox

# Firebase database 인증 및 앱 초기화


cred = credentials.Certificate('key.json')
firebase_admin.initialize_app(cred)

db = firestore.client()



"""user = auth.get_user(None)"""

results = []
results2 = []

window = Tk()
window.title('불량제품 검사')
window.geometry('600x600+500+100')
window.resizable(False, False)
# 사용자 id와 password를 저장하는 변수 생성
user_id, userID, password = StringVar(), StringVar(), StringVar()

user_round, user_area, User_ID= StringVar(), StringVar(), StringVar()




def inputValue():
    try:
        user = ent1.get()
        uID = auth.get_user_by_email(user)
        print('Successfully fetched user data: {0}'.format(uID.uid))

        window.destroy()
        window2 = Tk()
        window2.title('불량제품 검사')
        window2.geometry('600x600+500+100')
        window2.resizable(False, False)

        label_main = Label(window2, text="정상 제품 기준치 입력")
        label_main.pack()

        label_ID = Label(window2)
        label_ID['text'] = '현재 접속한 ID : ' + user
        label_ID.pack()

        label_round = Label(window2, text="둘레를 입력하세요.")
        label_round.pack()

        ent_round = Entry(window2)
        ent_round.pack()

        label_area = Label(window2, text="넓이를 입력하세요.")
        label_area.pack()

        ent_area = Entry(window2)
        ent_area.pack()

        btn_register = Button(window2, text="등록", command=lambda : messagePrint(user, window2, ent_round.get(), ent_area.get()))
        btn_register.pack()

        window2.mainloop()

    except:
        print("오류")


##메시지 박스
def messagePrint(id, w, round, area):

    print('아이디:', id, round)
    msg = tkinter.messagebox.askquestion('등록 완료', '제품 검사를 진행하시겠습니까?')
    if msg == 'yes':
        print('진행')



        ##검사 진행
        w.destroy()
        checkStart(id,round, area)


    else:
        tkinter.messagebox.showinfo('취소', '취소되었습니다.')

## 제품 측정 시작
def checkStart(id, round, area):
    window3 = Tk()
    window3.title('불량제품 검사')
    window3.geometry('600x600+500+100')
    window3.resizable(False, False)
    Label(window3, text="검사 진행 제품 측정").grid(row=0, column=0, padx=10, pady=10)

    ##임의값 생성(테스트용)

    result_round =[]
    result_area = []

    ##둘레
    for i in range(1,6):
        x = random.randrange(10, 20)
        result_round.append(x)
        print(result_round)
    ##넓이
    for i in range(1, 6):
        x = random.randrange(10, 20)
        result_area.append(x)
        print( result_area)

    number = 0
    for test in result_round:
        number = number+1 ##순서
        ##정상일 때
        if test == int(round): ##정상 조건
            print("%d번 정상" % number)
            ## 데이터 DB에 전송
            now = datetime.now() ##시간
            doc_ref = db.collection(id).document(str(number))
            doc_ref.set({
                u'normal_round': result_round[number-1], ##배열[number]하면 배열[1]부터 시작하기 때문에 배열[0]부터 하기위해서 -1을 함.
                u'normal_area': result_area[number-1],
                u'User': id,
                u'result': '정상',
                u'time': str(now)
            })
        ##불량일 때
        else:
            print("%d번 불량" % number)
            ## 데이터 DB에 전송
            now = datetime.now()
            doc_ref = db.collection(id).document(str(number))
            doc_ref.set({
                u'normal_round': result_round[number - 1],
                u'normal_area': result_area[number - 1],
                u'User': id,
                u'result': '불량',
                u'time': str(now)
            })


label = Label(window)
label['text'] = '아이디'
label.grid(row=0, column=0)
label.pack()

label2 = Label(window)


def id(n):
    label2.config(text="입력한 아이디 : " + ent1.get())


ent1 = Entry(window)
ent1.bind("<Return>", id)
ent1.pack()
label2.pack()

labPW = Label(window)
labPW['text'] = '비밀번호'
labPW.pack()

labPW2 = Label(window)


def pw(n):
    labPW2.config(text="입력한 비밀번호 : " + ent2.get())


ent2 = Entry(window)
ent2.bind("<Return>", pw)
ent2.pack()
labPW2.pack()


def changeFrame():
    try:
        user = ent1.get()
        uID = auth.get_user_by_email(user)
        print('Successfully fetched user data: {0}'.format(uID.uid))

    except:
        print("오류")

btnLogin = Button(window, text="로그인", command=inputValue)
btnLogin.pack()

window.mainloop()







