import time

def getClassFromServer(room,day,sock):
    cNumTimes = []
    sock.sendall('0'.encode())
    sock.recv(1024).decode()
    senddata = room + ',' + day
    sock.sendall(senddata.encode())

    data = sock.recv(1024).decode()
    if not data:
        print('error')
        return
    count = int(data)
    i=0
    while i < count:
        sock.sendall('ok'.encode())
        cNumTime = sock.recv(1024).decode()
        cNumTimes.append(cNumTime)
        i = i + 1
    
    return cNumTimes
    

def getNameFromServer(classnum,sock):
    names = []
    sock.sendall('1'.encode())
    sock.recv(1024).decode()
    senddata = classnum
    sock.sendall(senddata.encode())

    data = sock.recv(1024).decode()
    if not data:
        print('error')
        return
    count = int(data)
    i=0
    while i < count:
        sock.sendall('ok'.encode())
        name = sock.recv(1024).decode()
        names.append(name)
        i = i + 1
  
    for name in names:
        data_transferred = 0

        sock.sendall('name_ok'.encode())
        size = sock.recv(1024).decode()
        sock.sendall('size_ok'.encode())

        data = sock.recv(1024)
        if not data:
            print('error')
            return
    
        with open(name+'.jpg','wb') as f:
            try:
                while data:
                    f.write(data)
                    data_transferred += len(data)
                    if data_transferred >= int(size):
                        size = 0
                        break
                    data = sock.recv(1024)
            except Exception as e:
                print(e)
        print('파일[%s] 다운완료. 파일크기 [%d]'%(name+'.jpg',data_transferred))
    return names

def sendAbsentToServer(classnum,names,sock):
    sock.sendall('2'.encode())
    sock.recv(1024).decode()

    senddata = classnum
    sock.sendall(senddata.encode())
    sock.recv(1024).decode()

    if names[0] != '':
        sock.sendall(names[0].encode())
        sock.recv(1024).decode()
    else:
        sock.sendall('0'.encode())
        sock.recv(1024).decode()

    if names[1] != '':
        sock.sendall(names[1].encode())
        sock.recv(1024).decode()
    else:
        sock.sendall('0'.encode())
        sock.recv(1024).decode()

    if names[2] != '':
        sock.sendall(names[2].encode())
        sock.recv(1024).decode()
    else:
        sock.sendall('0'.encode())
        sock.recv(1024).decode()