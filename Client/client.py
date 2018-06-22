import time
import threading
import socket
import face_recognition
import cv2
import clientNetModule as cm
import faceModule as fm
import os
from multiprocessing import Process,Queue



#시간 관련 변수 init
days = ['월','화','수','목','금','토','일']
now = time.localtime()  #현재시간
nowSec = now.tm_hour * 3600 + now.tm_min * 60 + now.tm_sec #현재 시간을 초로 계산 

#network 관련 변수 init
HOST = 'faceserver.gq'
PORT = 9008
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST,PORT))

#names, cNumTimes init
names = []
cNumTimes = []

device = 0

def GetStartTime(time_string): #다음 수업시작 30분전 초 구하는 함수
    time_string = time_string.split(':')
    h = int(time_string[0])
    m = int(time_string[1])
    targetSec = (h-1)*3600 + (m+30)*60 + 00 
    return  targetSec

def facecheck(known_face_encodings,names,class_time,classnum,q):
    video = cv2.VideoCapture(0)
    check_students = fm.match_face(video,known_face_encodings,names,class_time,classnum)
    if check_students == 0:
        check_students = fm.match_face(video,known_face_encodings,names,class_time,classnum)
    video.release()
    q.put(check_students)

def Pass():
    q = Queue()
    print('-출석 시작-')
    #학생 이름 및 이미지 파일 가져오기
    cNumTime = cNumTimes.pop()
    cNumTime = cNumTime.split(',')
    classnum = cNumTime[1]
    names = cm.getNameFromServer(classnum,sock)

    #이미지 파일 이용하여 출석 체크 --> -30분 ~ 정시(출석) 정시 ~ +10분(지각) +10분 ~ (결석)
    known_face_encodings = []

    for name in names:
        path = name+'.jpg'
        known_face_encodings.append(fm.make_faceencoding(path))

    p = Process(target=facecheck,args=(known_face_encodings,names,cNumTime[0],classnum,q))
    p.start()
    p.join()
    check_students = q.get()
    q.close()

    #출결 후 출석자 지각자 결석자 서버로 전송
    cm.sendAbsentToServer(classnum,check_students,sock)
    for name in names:
        path =  name+'.jpg'
        os.remove(path)

if __name__ == '__main__':
    room = input('강의실 입력:') #최초의 프로그램 실행 시 해당 강의실 입력
    
    while True:
        print('-강의 목록 준비-')
        day = days[now.tm_wday]
        
        oldcNumTimes = cm.getClassFromServer(room,day,sock) #임의로 '금' 요일로 설정(day를 넣어야함)
        oldcNumTimes.sort()

        if(len(oldcNumTimes) > 0):
            for cNumTime in oldcNumTimes:
                ctime = cNumTime.split(',')[0]
                ctime = ctime.split(':')
                if(now.tm_hour < int(ctime[0])):
                    cNumTimes.append(cNumTime)
            cNumTimes.reverse()
            print(cNumTimes)
            if (len(cNumTimes) > 0):
                while True:
                    print('-출석 준비-')
                    start_time = cNumTimes[-1].split(',')[0]
                    targetSec = GetStartTime(start_time)  # 원하는 target시간(초단위)
                    now = time.localtime()
                    nowSec = now.tm_hour * 3600 + now.tm_min * 60 + now.tm_sec
                    remainingSec = targetSec - nowSec  # targetSec까지 남은 시간
                    if remainingSec < 0:
                        remainingSec = 0
                    print(remainingSec)
                    t = threading.Timer(1, Pass) #임의로 1초 대기로 설정(remainingSec을 넣어야함)
                    t.start()

                    t.join()
                    if(len(cNumTimes) == 0):
                        break
        
        print('오늘의 강의 모두 출석 완료. 다음날 까지 대기...')
        while True:
            if(day == days[now.tm_wday]):
                time.sleep(8*3600) # 수정 필요 -> 다음 날까지의 시간계산해서 잠들기 코드
            else:
                break