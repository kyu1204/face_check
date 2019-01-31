졸업프로젝트
===========
face_recognition을 이용한 얼굴인식 출석체크
------------------------------------------
**Use Python**
>(*클라이언트-> dlib, face_recognition 설치 필수*)
* * *
# Server
1. 클라이언트에서 오늘 요일과 강의실 정보를 서버로 전송, 서버는 해당 정보를 이용하여 DB에서 해당하는 요일과 강의실에 수업 정보를 패킷으로 전송
>(*class_Num, start_time*)

2. 클라이언트에서 수업코드를 서버로 전송, 서버는 DB에서 수업코드를 이용하여 해당 수업을 듣는 학생의 이름, 사진 파일(*스토리지 경로*)을 검색 해당하는 **이름과 사진 파일**을 클라이언트로 전송

![server1](https://kyu1204.github.io/face/server.JPG)
>*그림1 이름과 사진파일 전송*

3. 클라이언트에서 출결 정보를 서버로 전송, 서버는 전달받은 출결 정보를 DB에 저장

![server2](https://kyu1204.github.io/face/server_2.JPG)
>*그림2 출결 정보를 받은 후 DB에 저장*

* * *
# Client
1. 처음 프로그램이 가동될 때에 입력받은 강의실 정보와 현재 날짜를 이용해 현재 요일을 구한 후 두 정보를 서버로 전송

![client1](https://kyu1204.github.io/face/client_1.JPG)
>*그림3 강의실 정보 입력*

2. 전달받은 수업 정보를 시간 순서에 맞게 정렬함. 그 후 수업 시간이 제일 빠른 수업코드를 가져와 수업 **시작 30분 전** 시간을 구한 후 슬립.

3. 수업 **시작 30분 전**이 되면 슬립에서 깨어나 해당 수업코드를 서버로 전송, 해당 수업을 듣는 학생들의 **이름 및 사진 파일**을 받아 저장함

![client2](https://kyu1204.github.io/face/client_2.JPG)
>*그림4 이름 및 사진파일을 서버로 부터 다운



![client2_2](https://kyu1204.github.io/face/client_2_2.JPG)
>*그림5 실제 디렉토리에 사진파일이 저장됨*

4. 사진 파일 다운로드가 완료되면 자식 프로세서를 생성, **얼굴인식 알고리즘**(*face_recognition*)을 구동함. 라이브 캠으로 얼굴을 인식 후 저장된 사진 파일과 비교, 해당하는 학생이면 출석을 진행함.
>(*시작 30분 전 ~ 수업 시작:출석, 수업 시작 ~ 10분 후:지각, 10분 후 ~ :결석*)

![client3](https://kyu1204.github.io/face/client_3.JPG)
>*그림6 출결 프로세서 실행


![client3_2](https://kyu1204.github.io/face/client_3_2.JPG)
>*그림7 실제 얼굴 인식 후 출석으로 처리*

5. 수업 시작 10분 후 출결이 전부 완료되면 해당 출결 정보를 서버로 전송 후 **다음 수업 시작 시간 30분 전**까지 슬립.

6. 수업 정보 테이블이 비게 되면 즉 그날의 수업이 모두 종료되면 **8시간 슬립**에 들어감. 슬립에서 깨어난 후 현재 시간에 따른 요일을 가져와 이전에 구한 요일과 비교 (*다음날이 되었는지 검사*), 바뀌지 않았으면 다시 8시간 슬립 바뀌었으면 다시 1번부터 반복.

* * *
# DB
Student_db 테이블 구조

![db1](https://kyu1204.github.io/face/db_class.JPG)
>*그림8 Class Table 구조*


![db2](https://kyu1204.github.io/face/db_student;.JPG)
>*그림9 Student Table 구조*


![db2](https://kyu1204.github.io/face/db_study.JPG)
>*그림9 Study Table 구조*


![db2](https://kyu1204.github.io/face/db_absent.JPG)
>*그림9 Absent Table 구조*
* * *
# 참고자료
**[OpenCV](https://opencv.org/)**

**[dlib](http://dlib.net/)**

**[face_recognition](https://github.com/ageitgey/face_recognition)**
