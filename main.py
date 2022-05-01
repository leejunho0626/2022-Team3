import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import auth
import random
from datetime import datetime
from tkinter import *
import tkinter.messagebox

# Firebase database 인증 및 앱 초기화


cred = credentials.Certificate('key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://teamproject-642cf-default-rtdb.firebaseio.com/'
    # 'databaseURL' : '데이터 베이스 url'
})

"""user = auth.get_user(None)"""

results = []
results2 = []

window = Tk()
window.title('불량제품 검사')
window.geometry('600x600+500+100')
window.resizable(False, False)
# 사용자 id와 password를 저장하는 변수 생성
user_id, userID, password = StringVar(), StringVar(), StringVar()

user_round, user_area = StringVar(), StringVar()


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
        Label(window2, text="정상 제품 기준치 입력").grid(row=0, column=0, padx=10, pady=10)
        Label(window2, text="현재 접속한 ID : " + user).grid(row=0, column=1, padx=10, pady=10)
        Label(window2, text="둘레를 입력하세요.").grid(row=1, column=0, padx=10, pady=10)
        Label(window2, text="넓이를 입력하세요.").grid(row=2, column=0, padx=10, pady=10)
        Entry(window2, textvariable=user_round).grid(row=1, column=1, padx=10, pady=10)
        Entry(window2, textvariable=user_area).grid(row=2, column=1, padx=10, pady=10)
        Button(window2, text="등록", command=lambda: messagePrint(user, window2)).grid(row=3, column=1, padx=10, pady=10)
        window2.mainloop()
    except:
        print("오류")


##메시지 박스
def messagePrint(id, w):
    print('아이디:', id)
    msg = tkinter.messagebox.askquestion('등록 완료', '제품 검사를 진행하시겠습니까?')
    if msg == 'yes':
        print('진행')
        ##검사 진행
        w.destroy()
        checkStart()


    else:
        tkinter.messagebox.showinfo('취소', '취소되었습니다.')


def checkStart():
    window3 = Tk()
    window3.title('불량제품 검사')
    window3.geometry('600x600+500+100')
    window3.resizable(False, False)
    Label(window3, text="검사 진행 1단계 제품 측정").grid(row=0, column=0, padx=10, pady=10)


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

"""
results = []
results2 = []
##라벨
label = Label(window)
label['text']='둘레를 입력하세요.'
label.pack()

label3 = Label(window)
def w(n):
    label3.config(text = "입력한 둘레 길이입니다. > "+ ent.get()+"cm")
    print('세로:', ent.get())
    results.append(ent.get())
##입력창
ent=Entry(window)
ent.bind("<Return>", w)
ent.pack()
label3.pack()

label2 = Label(window)
label2['text']=' 면적을 입력하세요.'
label2.pack()

label4 = Label(window)
def h(n):
    label4.config(text = "입력한 면적 크기입니다. > "+ ent2.get()+"cm")
    print('세로:', ent2.get())
    results2.append(ent2.get())
    print(results, results2)


    a=4
    abc = '제품' + str(a)
    now = datetime.now()
    # db 위치 지정, 기본 가장 상단을 가르킴
    ref = db.reference(abc)  # 경로가 없으면 생성한다.
    ref.update({'둘레': ent.get()})
    ref.update({'면적': ent2.get()})
    ref.update({'시간': str(now)})
    ref.update({'ID': "test"})


##입력창
ent2=Entry(window)
ent2.bind("<Return>", h)
ent2.pack()
label4.pack()
"""

window.mainloop()







