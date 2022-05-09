import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import auth
from firebase_admin import firestore
import random
from datetime import datetime
from tkinter import *
import tkinter.messagebox
import tkinter.font as tkFont

# Firebase database 인증 및 앱 초기화(Realtime Database, Firestore Database)
cred = credentials.Certificate('key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://teamproject-642cf-default-rtdb.firebaseio.com/'
    # 'databaseURL' : '데이터 베이스 url'
})  # Realtime Database
database = firestore.client()  # Firestore Database


# 정상 기준치 입력 화면
def inputValue(id, pw, window):
    try:
        user = id


        window.destroy()  # 이전 프레임 종료
        window2 = Tk()
        window2.title('제품 검사 프로그램')
        window2.geometry('400x400+700+300')
        window2.resizable(False, False)
        window2.config(bg='orange')

        label_main = Label(window2, text="\n정상 제품 기준치 입력", bg='orange')
        label_main.pack()

        label_ID = Label(window2, bg='orange')
        label_ID['text'] = '현재 접속한 ID : ' + user
        label_ID.pack()

        label_round = Label(window2, text="\n둘레를 입력하세요.", bg='orange')
        label_round.pack()

        ent_round = Entry(window2)
        ent_round.pack()

        label_area = Label(window2, text="넓이를 입력하세요.", bg='orange')
        label_area.pack()

        ent_area = Entry(window2)
        ent_area.pack()

        btn_register = Button(window2, text="등록",
                              command=lambda: messagePrint(user, window2, ent_round.get(), ent_area.get()))
        btn_register.pack()

        window2.mainloop()

    except:
        print("오류")
        msg = tkinter.messagebox.showinfo('로그인 실패', '입력한 정보가 올바르지 않습니다.')


# 계정 생성 화면
def createUser(id, pw, window):
    print(id, pw)
    msg = tkinter.messagebox.askquestion('회원가입', '회원가입을 하시겠습니까?')
    if msg == 'yes':
        print('네')

        user = auth.create_user(
            email=id,
            email_verified=False,
            password=pw)

        ref = db.reference(user.uid)
        ref.update({'id': id})
        ref.update({'pw': pw})

        print('회원가입 완료')
        window.destroy()
        signIn()

    else:
        tkinter.messagebox.showinfo('취소', '취소되었습니다.')


# 회원 가입 화면
def signUp(window):
    window.destroy()
    window4 = Tk()
    window4.title('제품 검사 프로그램')
    window4.geometry('400x300+700+300')
    window4.resizable(False, False)
    window4.config(bg='orange')
    font2 = tkFont.Font(family="맑은 고딕", size=15, weight="bold")

    labSignUp = Label(window4, bg='orange', font=font2)
    labSignUp['text'] = '회원가입'
    labSignUp.grid(row=0, column=3)

    labuID = Label(window4, bg='orange', font=font2)
    labuID['text'] = 'ID'
    labuID.grid(row=1, column=2, padx=50, pady=10)

    entuID = Entry(window4)
    entuID.grid(row=1, column=3)

    labuPW = Label(window4, bg='orange', font=font2)
    labuPW['text'] = 'PW'
    labuPW.grid(row=2, column=2, padx=50)

    entuPW = Entry(window4)
    entuPW.config(show="*")
    entuPW.grid(row=2, column=3)

    btnRegister = Button(window4, text="가입하기",
                         command=lambda: createUser(entuID.get(), entuPW.get(), window4),
                         width=20, height=1, relief='solid')
    btnRegister.grid(row=3, column=3, pady=10)
    btnRegister.config(fg='blue')

    btnReturn = Button(window4, text="← 이전으로",
                       command=lambda: [window4.destroy(), signIn()], width=20, height=1, relief='solid')
    btnReturn.grid(row=4, column=3)
    btnReturn.config(fg='blue')

    window4.mainloop()


# 제품 검사 진행 메시지 박스
def messagePrint(id, w, round, area):
    print('아이디:', id, round)
    msg = tkinter.messagebox.askquestion('등록 완료', '제품 검사를 진행하시겠습니까?')
    if msg == 'yes':
        print('진행')

        ##검사 진행
        w.destroy()
        checkStart(id, round, area)


    else:
        tkinter.messagebox.showinfo('취소', '취소되었습니다.')


# 제품 측정 시작 화면
def checkStart(id, round, area):
    window3 = Tk()
    window3.title('불량제품 검사')
    window3.geometry('600x600+500+100')
    window3.resizable(False, False)
    Label(window3, text="검사 진행 제품 측정").grid(row=0, column=0, padx=10, pady=10)

    # 임의값 생성(테스트용)

    result_round = []
    result_area = []

    # 둘레
    for i in range(1, 6):
        x = random.randrange(10, 20)
        result_round.append(x)
        print(result_round)
    # 넓이
    for i in range(1, 6):
        x = random.randrange(10, 20)
        result_area.append(x)
        print(result_area)

    number = 0
    for test in result_round:
        number = number + 1  # 순서
        # 정상일 때
        if test == int(round):  # 정상 조건
            print("%d번 정상" % number)
            # 데이터 DB에 전송
            now = datetime.now()  # 시간
            doc_ref = database.collection(id).document(str(number))
            doc_ref.set({
                u'round': result_round[number - 1],  # 배열[number]하면 배열[1]부터 시작하기 때문에 배열[0]부터 하기위해서 -1을 함.
                u'area': result_area[number - 1],
                u'user': id,
                u'result': '정상',
                u'time': str(now.strftime('%Y-%m-%d %H:%M:%S'))
            })
        # 불량일 때
        else:
            print("%d번 불량" % number)
            # 데이터 DB에 전송
            now = datetime.now()
            doc_ref = database.collection(id).document(str(number))
            doc_ref.set({
                u'round': result_round[number - 1],
                u'area': result_area[number - 1],
                u'user': id,
                u'result': '불량',
                u'time': str(now.strftime('%Y-%m-%d %H:%M:%S'))
            })


# 로그인 판단
def checkInfo(id, pw, window):
    try:
        userID = id
        userPW = pw

        uid = auth.get_user_by_email(id)
        ref = db.reference(uid.uid).child('pw')
        # 아이디와 비밀번호를 입력한 경우
        if len(userID) & len(userPW) > 0:

            if userPW == ref.get():
                inputValue(id, pw, window)
            else:
                tkinter.messagebox.showinfo('Fail', '아이디 또는 비밀번호가 틀렸습니다.')
        # 아이디와 비밀번호를 입력하지 않은 경우
        else:
            tkinter.messagebox.showinfo('Fail', '아이디 또는 비밀번호를 입력하세요.')
    except:
        tkinter.messagebox.showinfo('Fail', '아이디 또는 비밀번호가 틀렸습니다.')



# 로그인 화면
def signIn():
    window = Tk()
    window.title('제품 검사 프로그램')
    window.geometry('400x300+700+300')
    window.resizable(False, False)
    window.config(bg='orange')
    font = tkFont.Font(family="맑은 고딕", size=15, weight="bold")
    labMain = Label(window, bg='orange', font=font)
    labMain['text'] = 'Error Detector'
    labMain.grid(row=0, column=3)

    labID = Label(window, bg='orange', font=font)
    labID['text'] = 'ID'
    labID.grid(row=1, column=2, padx=50, pady=10)

    ent1 = Entry(window)
    ent1.grid(row=1, column=3)

    labPW = Label(window, bg='orange', font=font)
    labPW['text'] = 'PW'
    labPW.grid(row=2, column=2, padx=50)

    ent2 = Entry(window)
    ent2.config(show="*")
    ent2.grid(row=2, column=3)

    btnLogin = Button(window, text="로그인", command=lambda: checkInfo(ent1.get(), ent2.get(), window), width=20,
                      height=1, relief='solid')
    btnLogin.grid(row=3, column=3, pady=10)
    btnLogin.config(fg='blue')

    btnSignUp = Button(window, text="회원가입", command=lambda: signUp(window), width=20, height=1, relief='solid')
    btnSignUp.grid(row=4, column=3)
    btnSignUp.config(fg='blue')

    window.mainloop()


signIn()  # 프로그램 시작(로그인 화면)
