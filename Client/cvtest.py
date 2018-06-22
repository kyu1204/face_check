import cv2
import time
from multiprocessing import Process



def Pass():
    v = cv2.VideoCapture(0)
    while True:
        ret, frame = v.read()
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    v.release()
 
    cv2.destroyAllWindows()
if __name__ == '__main__':
    i=0
    while i < 3: 
        t = Process(target=Pass)
        t.start()
        
        t.join()
        i+=1
