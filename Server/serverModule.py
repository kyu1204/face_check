import socketserver
from os.path import exists
import pymysql
import os
import datetime as dt

class MyTcpHandler(socketserver.BaseRequestHandler):
    students = []
    def handle(self):  
        print('[%s] 연결됨' %self.client_address[0])
        flag = self.request.recv(1024)
        flag = flag.decode()
        self.request.send("ok".encode())

        if flag == '0':
            recvdata = self.request.recv(1024)
            recvdata = recvdata.decode()
            recvdata = recvdata.split(',')
            room = recvdata[0]
            day = recvdata[1]

            con = pymysql.connect(host='localhost',user='minkyu',passwd='12345678',db='student_db',charset='utf8')
            cur = con.cursor()
            cur.execute('select start_time,cNum from class where day=%s && room=%s',(day,room))
            cNumTimes = cur.fetchall()
            count = len(cNumTimes)

            self.request.send(str(count).encode())
            for cNumTime in cNumTimes:
                self.request.recv(1024)
                senddata = cNumTime[0]+','+cNumTime[1]
                self.request.send(senddata.encode())

        if flag == '1': #이미지 파일전송 부분/////////////////////////////////////////////////////////////////
            recvdata = self.request.recv(1024) # 클라이언트로 부터 파일이름을 전달받음
            recvdata = recvdata.decode() # 파일이름 이진 바이트 스트림 데이터를 일반 문자열로 변환

            con = pymysql.connect(host='localhost',user='minkyu',passwd='12345678',db='student_db',charset='utf8')
            cur = con.cursor()
            cur.execute('select name,img from student where id in (select student_id from study where class_num=%s)',recvdata)
            students = cur.fetchall()
            count = len(students)

            self.request.send(str(count).encode())
            for student in students:
                self.request.recv(1024)
                senddata = student[0]
                self.request.send(senddata.encode())

            for student in students:
                recvdata = self.request.recv(1024)
                recvdata = recvdata.decode()
                
                data_transferred = 0
                if not exists(student[1]): # 파일이 해당 디렉터리에 존재하지 않으면
                    return # handle()함수를 빠져 나온다.
                size = os.path.getsize(student[1])
                size = str(size)
                self.request.send(size.encode())
                recvdata = self.request.recv(1024)

                print('파일[%s] 전송 시작...' %student[1])
                with open(student[1], 'rb') as f:
                    try:
                        data = f.read(1024) # 파일을 1024바이트 읽음
                        while data: # 파일이 빈 문자열일때까지 반복
                            data_transferred += self.request.send(data)
                            data = f.read(1024)
                    except Exception as e:
                        print(e)
                print('전송완료[%s], 전송량[%d]' %(student[1],data_transferred))

        if flag == '2': #출결정보 DB 업로드 분 //////////////////////////////////////////////////////
            date=str(dt.datetime.now()).split('.')[0]
            classnum = self.request.recv(1024) # 과목코드
            classnum = classnum.decode()
            self.request.send('class_ok'.encode())

            passStudents = self.request.recv(1024) # 출석자 명단
            passStudents = passStudents.decode() # 파일이름 이진 바이트 스트림 데이터를 일반 문자열로 변환
            self.request.send('pass_ok'.encode())
            if passStudents == '0':
                passStudents = ''

            lateStudents = self.request.recv(1024) # 지각자 명단
            lateStudents = lateStudents.decode()
            self.request.send('late_ok'.encode())
            if lateStudents == '0':
                lateStudents = ''

            absentStudents = self.request.recv(1024) # 결석자 명단
            absentStudents = absentStudents.decode()
            self.request.send('absent_ok'.encode())
            if absentStudents == '0':
                absentStudents = ''

            con = pymysql.connect(host='localhost',user='minkyu',passwd='12345678',db='student_db',charset='utf8')
            cur = con.cursor()
            cur.execute('insert into absent (class_num,pass_students,late_students,absent_students,time) values(%s,%s,%s,%s,%s)',(classnum,passStudents,lateStudents,absentStudents,date))
            con.commit()
 
 
def runServer(HOST,PORT):
    print('++++++파일 서버를 시작++++++')
    print("+++파일 서버를 끝내려면 'Ctrl + C'를 누르세요.")
 
    try:
        server = socketserver.TCPServer((HOST,PORT),MyTcpHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print('++++++파일 서버를 종료합니다.++++++')