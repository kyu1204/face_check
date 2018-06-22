import face_recognition
import cv2
import time

def replaceRight(original, old, new, count_right):
    repeat=0
    text = original
    
    count_find = original.count(old)
    if count_right > count_find : # 바꿀 횟수가 문자열에 포함된 old보다 많다면
        repeat = count_find # 문자열에 포함된 old의 모든 개수(count_find)만큼 교체한다
    else :
        repeat = count_right # 아니라면 입력받은 개수(count)만큼 교체한다

    for _ in range(repeat):
        find_index = text.rfind(old) # 오른쪽부터 index를 찾기위해 rfind 사용
        text = text[:find_index] + new + text[find_index+1:]
    
    return text

def GetSec(time_string): #다음 수업시작 30분전 초 구하는 함수
    
    time_string = time_string.split(':')
    h = int(time_string[0])
    m = int(time_string[1])
    targetSec = h*3600 + m*60 + 00 
    return  targetSec

def make_faceencoding(filename):
    image = face_recognition.load_image_file(filename)
    encoding = face_recognition.face_encodings(image)[0]
    return encoding

def match_face(video,known_face_encodings,names,class_time,classnum):
    print('녹화시작-'+classnum)
    if not video.isOpened():
        video.open()
    pass_s = []
    late_s = []
    students = []
    class_time = GetSec(class_time)
    face_locations = []
    face_encodings = []
    process_this_frame = True

    while True:
        ret, frame = video.read()
        if not ret:
            return 0
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        if process_this_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding,0.46)
                name = "Unknown"

                if True in matches:
                    first_match_index = matches.index(True)
                    name = names[first_match_index]
                    now = time.localtime()
                    nowSec = now.tm_hour * 3600 + now.tm_min * 60 + now.tm_sec
                    
                    if not(name in students):
                        students.append(name)
                        if(nowSec <= class_time):
                            pass_s.append(name)
                        if(nowSec > class_time and nowSec <= (class_time+600)):
                            late_s.append(name)
                            name = 'Late'

                    if(nowSec <= class_time):
                        name = 'Pass'
                    if(nowSec > class_time and nowSec <= (class_time+600)):
                        name = 'Late'
                face_names.append(name)

        process_this_frame = not process_this_frame

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        cv2.imshow(classnum, frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        #시간 검사해서 10분이 지난후 자동 종료되는 코드
        now = time.localtime()
        nowSec = now.tm_hour * 3600 + now.tm_min * 60 + now.tm_sec
        if nowSec > (class_time+601):
            break
            
    # Release handle to the webcam
    cv2.destroyWindow(classnum)

    pass_string = ''
    late_string = ''
    absent_string = ''

    for stu in pass_s:
        pass_string += stu + ','

    for stu in late_s:
        late_string += stu + ','

    for stu in names:
        if not(stu in students):
            absent_string += stu + ','

    pass_string = replaceRight(pass_string,',','',1)
    late_string = replaceRight(late_string,',','',1)
    absent_string = replaceRight(absent_string,',','',1)

    check_names = [pass_string,late_string,absent_string]
    return check_names