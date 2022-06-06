from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import auth
from firebase_admin import firestore
from tkinter import *
import tkinter.messagebox
import tkinter.font as tkFont
from tkinter import filedialog
import shutil
import os
import measure_object_size

# Firebase database 인증 및 앱 초기화(Realtime Database, Firestore Database)
cred = credentials.Certificate('key.json')

database = firestore.client()  # Firestore Database

route = "C:/3Team/img.jpg"  ## 이미지 저장 경로


# 정상 기준치 입력 화면
def inputValue(id, window):
    try:
        user = id  # 접속한 사용자 ID
        window.destroy()  # 이전 프레임 종료
        window2 = Tk()
        window2.title('Error Detector')
        window2.geometry('450x350+600+200')
        window2.iconbitmap('team3.ico')
        window2.resizable(False, False)
        window2.config(bg='orange')
        font3 = tkFont.Font(family="맑은 고딕", size=15, weight="bold")
        font4 = tkFont.Font(family="맑은 고딕", size=10, weight="bold")
        label_main = Label(window2, text="\n  정상 제품 기준치 입력", bg='orange', font=font3)
        label_main.grid(row=0, column=2, columnspan=2)

        label_ID = Label(window2, bg='orange', font=("맑은 고딕", 10, "bold"))
        label_ID['text'] = '현재 접속한 ID : '
        label_ID.grid(row=1, column=2, padx=70)

        label_User = Label(window2, bg='orange', font=("맑은 고딕", 10, "bold"))
        label_User['text'] = user
        label_User.grid(row=1, column=3)

        label_round = Label(window2, text="둘레를 입력하세요.", bg='orange', font=("맑은 고딕", 10, "bold"))
        label_round.grid(row=2, column=2)

        ent_round = Entry(window2)
        ent_round.grid(row=2, column=3, pady=3)
        ent_round.config(highlightthickness=1)

        label_area = Label(window2, text="넓이를 입력하세요.", bg='orange', font=("맑은 고딕", 10, "bold"))
        label_area.grid(row=3, column=2)

        ent_area = Entry(window2)
        ent_area.grid(row=3, column=3, pady=3)
        ent_area.config(highlightthickness=1)

        btn_imgRegister = Button(window2, text="사진 선택",
                                 command=lambda: fLoad(window2),
                                 width=20, height=1, relief='raised'
                                 )

        btn_imgRegister.grid(row=4, column=3, pady=3)

        label_img = Label(window2, text="사진을 등록하세요.", bg='orange', font=("맑은 고딕", 10, "bold"))
        label_img.grid(row=4, column=2)

        btn_imgRegister = Button(window2, text="카메라 테스트",
                                 command=lambda: measure_object_size.onlyVideo(),
                                 width=20, height=1, relief='raised'
                                 )

        btn_imgRegister.grid(row=7, column=3, pady=3)

        btn_imgRegister = Button(window2, text="스케일 측정",
                                 command=lambda: measure_object_size.playscale(user),
                                 width=20, height=1, relief='raised'
                                 )

        btn_imgRegister.grid(row=8, column=3, pady=3)

        btn_register = Button(window2, text="검사 시작",
                              command=lambda: measure_object_size.playVideo(route, user, ent_round.get(),
                                                                            ent_area.get()),
                              width=20, height=1, relief='solid', font=font4
                              )
        btn_register.grid(row=9, column=3, pady=10)
        btn_register.config(fg='blue')

        window2.mainloop()

    except:
        print("오류")
        msg = tkinter.messagebox.showinfo('로그인 실패', '입력한 정보가 올바르지 않습니다.')


# 스케일 측정 확인 메시지
def scaleMsg():
    tkinter.messagebox.showinfo('스케일 측정', '스케일 측정이 자동으로 되었습니다.')


# 파일 선택
def fLoad(window):
    img = filedialog.askopenfilename(initialdir='/', title="select a file", )  # 파일 선택, 선택한 파일 경로를 img 변수에 저장
    window.iconbitmap('team3.ico')
    label_imgFile = Label(window, text=img, bg='orange', font=("맑은 고딕", 10))  # 선택한 파일 경로 표시
    label_imgFile.grid(row=5, column=2, columnspan=2)
    print("경로", img)
    root_dir = 'C:/3Team'
    try:
        os.mkdir(root_dir)  # 폴더 생성
    except OSError:
        if not os.path.isdir(root_dir):
            raise

    route = "C:/3Team/img.jpg"  # 새로 복사할 경로

    try:
        shutil.copyfile(img, route)
    except:
        tkinter.messagebox.showinfo('사진 선택 오류', '사진을 다시 선택해주세요.')


# 크기 값 받아오기
def size_data(round, area):
    r = round
    a = area

    print('둘레 : ' + r + '넓이 : ' + a)


# 계정 생성
def createUser(id, pw, window):
    try:
        print(len(id), len(pw))
        msg = tkinter.messagebox.askquestion('회원가입', '회원가입을 하시겠습니까?')
        if msg == 'yes':
            user = auth.create_user(
                email=id,
                email_verified=False,
                password=pw)
            ref = db.reference(user.uid)
            ref.update({'id': id})
            ref.update({'pw': pw})
            print('회원가입 완료')
            tkinter.messagebox.showinfo('회원가입 완료', '가입에 성공하였습니다.')
            window.destroy()
            signIn()
        else:
            tkinter.messagebox.showinfo('취소', '취소되었습니다.')
    except:
        tkinter.messagebox.showinfo('회원가입 실패', '회원가입에 실패했습니다.(중복된 아이디 또는 아이디&비빌번호가 입력되지 않았습니다.')


# 회원 가입 화면
def signUp(window):
    window.destroy()
    window4 = Tk()
    window4.title('Error Detector')
    window4.geometry('450x300+600+200')
    window4.iconbitmap('team3.ico')
    window4.resizable(False, False)
    window4.config(bg='orange')
    font2 = tkFont.Font(family="맑은 고딕", size=15, weight="bold")
    font3 = tkFont.Font(family="맑은 고딕", size=12, weight="bold")
    font4 = tkFont.Font(family="맑은 고딕", size=8, weight="bold")

    labSignUp = Label(window4, bg='orange', font=font2)
    labSignUp['text'] = '\n회원가입\n'
    labSignUp.grid(row=0, column=1)

    labuID = Label(window4, bg='orange', font=font3)
    labuID['text'] = '아이디(이메일)'
    labuID.grid(row=1, column=1, padx=170)

    entuID = Entry(window4)
    entuID.grid(row=2, column=1)
    entuID.config(highlightthickness=1)

    labuPW = Label(window4, bg='orange', font=font3)
    labuPW['text'] = '비밀번호'
    labuPW.grid(row=3, column=1, padx=50)

    entuPW = Entry(window4)
    entuPW.config(show="*")
    entuPW.grid(row=4, column=1)
    entuPW.config(highlightthickness=1)

    btnRegister = Button(window4, text="가입하기",
                         command=lambda: createUser(entuID.get(), entuPW.get(), window4),
                         width=20, height=1, relief='solid', font=font4)
    btnRegister.grid(row=5, column=1, pady=10)
    btnRegister.config(fg='blue')

    btnReturn = Button(window4, text="← 이전으로",
                       command=lambda: [window4.destroy(), signIn()], width=20, height=1, relief='solid', font=font4)
    btnReturn.grid(row=6, column=1)
    btnReturn.config(fg='red')

    window4.mainloop()


# 로그인 판단
def checkInfo(id, pw, window):
    try:
        userID = id
        userPW = pw

        uid = auth.get_user_by_email(id)
        ref = db.reference(uid.uid).child('pw')
        # 아이디와 비밀번호를 입력한 경우
        if len(userID) & len(userPW) > 0:
            # 비밀번호가 올바른 경우
            if userPW == ref.get():
                inputValue(id, window)  # 정상 기준치 입력 화면으로 이동
            # 비밀번호가 틀린 경우
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
    window.title('Error Detector')
    window.geometry('400x300+600+200')
    window.iconbitmap('team3.ico')
    window.resizable(False, False)
    window.config(bg='orange')
    font = tkFont.Font(family="맑은 고딕", size=12, weight="bold")
    labMain = Label(window, bg='orange', font=font)
    labMain['text'] = '\n\n Error Detector\n'
    labMain.grid(row=0, column=3)

    labID = Label(window, bg='orange', font=font)
    labID['text'] = '아이디(이메일)'
    labID.grid(row=1, column=2)

    ent1 = Entry(window, font=("맑은 고딕", 10, "bold"))
    ent1.grid(row=1, column=3)
    ent1.config(highlightthickness=1)

    labPW = Label(window, bg='orange', font=font)
    labPW['text'] = '비밀번호'
    labPW.grid(row=2, column=2, padx=50)

    ent2 = Entry(window, font=("맑은 고딕", 10, "bold"))
    ent2.config(show="*")  # 입력한 비밀번호 암호화
    ent2.grid(row=2, column=3)
    ent2.config(highlightthickness=1)

    btnLogin = Button(window, text="로그인",
                      command=lambda: checkInfo(ent1.get(), ent2.get(), window),
                      width=20, height=1, relief='solid', font=("맑은 고딕", 10, "bold"))  # 로그인 판단
    btnLogin.grid(row=3, column=3, pady=10)
    btnLogin.config(fg='blue')

    btnSignUp = Button(window, text="회원가입",
                       command=lambda: signUp(window),
                       width=20, height=1, relief='solid', font=("맑은 고딕", 10, "bold"))  # 회원가입 화면으로 이동
    btnSignUp.grid(row=4, column=3)

    window.mainloop()


signIn()  # 프로그램 시작(로그인 화면)