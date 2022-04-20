import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import random
from datetime import datetime
from tkinter import *

#Firebase database 인증 및 앱 초기화
cred = credentials.Certificate('key.json')
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://teamproject-642cf-default-rtdb.firebaseio.com/'
    #'databaseURL' : '데이터 베이스 url'
})

window = Tk()
window.title('불량제품 검사')
window.geometry('600x600')
window.resizable(False, False)

results = []
results2 = []

label = Label(window)
label['text']='둘레를 입력하세요.'
label.pack()

label3 = Label(window)
def w(n):
    label3.config(text = "입력한 둘레 길이입니다. > "+ ent.get()+"cm")
    print('세로:', ent.get())
    results.append(ent.get())

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
    now = "2022-04-20 17:28:09"
    # db 위치 지정, 기본 가장 상단을 가르킴
    ref = db.reference(abc)  # 경로가 없으면 생성한다.
    ref.update({'둘레': ent.get()})
    ref.update({'면적': ent2.get()})
    ref.update({'시간': str(now)})
    ref.update({'ID': "test"})


ent2=Entry(window)
ent2.bind("<Return>", h)
ent2.pack()
label4.pack()

window.mainloop()









