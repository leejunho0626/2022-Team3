import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

#Firebase database 인증 및 앱 초기화
cred = credentials.Certificate('key.json')
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://teamproject-642cf-default-rtdb.firebaseio.com/'
    #'databaseURL' : '데이터 베이스 url'
})

#db 위치 지정, 기본 가장 상단을 가르킴
ref = db.reference('Result/제품2') #경로가 없으면 생성한다.
ref.update({'가로' : '20'})
ref.update({'세로' : '20'})

#데이터 읽기
ref = db.reference('불량검사 결과')
print(ref.get()) #json형태로 받아와 진다. list로 반환


