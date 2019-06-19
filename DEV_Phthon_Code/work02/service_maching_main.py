import os
os.environ['OPENCV_IO_MAX_IMAGE_PIXELS']=str(2**64)
import cv2
import cv2
import numpy as np
import time
import threading


find_org_tmp = "./paris_baguette/pstart1.jpg"
fileSize = [320,180]
fileArray = [1,2,3,4,5]
keyLoop = 0
lock = threading.Lock()
oldFileName = 0



cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # CV_CAP_PROP_FRAME_WIDTH
cap.set(4, 720)  # CV_CAP_PROP_FRAME_HEIGHT
# cam.set(5, 0)  # CV_CAP_PROP_FPSq
print("VideoCapture Loading Success.....")
print('width :%d, height : %d' % (cap.get(3), cap.get(4)))


while(True):
    print("Start engin ...")
    ret, frame = cap.read()    # Read 결과와 frame
    print(ret)
    if(ret) :

        gray = cv2.cvtColor(frame,  cv2.COLOR_BGR2GRAY)    # 입력 받은 화면 Gray로 변환

        template = cv2.imread(find_org_tmp, 0)
        w, h = template.shape[::-1]

        gray.astype(np.float32)
        gray.astype(np.uint8)
        res = cv2.matchTemplate(gray, gray, cv2.TM_CCOEFF_NORMED)


        cv2.imshow('frame_color', frame)    # 컬러 화면 출력
        cv2.imshow('frame_gray', gray)    # Gray 화면 출력
        if cv2.waitKey(1) == ord('q'):
            break
    else:
        cap = cv2.VideoCapture(0)
        cap.set(3, 1280)  # CV_CAP_PROP_FRAME_WIDTH
        cap.set(4, 720)  # CV_CAP_PROP_FRAME_HEIGHT
        print("=====================================restart===========================================")

cap.release()
cv2.destroyAllWindows()
