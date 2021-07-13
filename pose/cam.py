import cv2 as cv

cap = cv.VideoCapture(0)

while(True):
    ret, cam = cap.read()

    if(ret) :
        cv.imshow('camera', cam)
        
        if cv.waitKey(1) & 0xFF == 27: # esc 키를 누르면 닫음
            break
                     
cap.release()
cv.destroyAllWindows()

import cv2
import numpy as np
def getFrames():
    video = cv2.VideoCapture('teknofest.mp4')
    ok, frame = video.read()
    count = 0
    while ok:
        cv2.imwrite("frame%d.jpg".format(count), frame)
        print('WRITTEN FRAME:',count)
        count+=1
        ok, frame = video.read()
    video.release()
getFrames()