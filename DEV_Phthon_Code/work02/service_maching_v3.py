import cv2
import numpy as np
import time
import matplotlib.pyplot as plt
import threading


cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # CV_CAP_PROP_FRAME_WIDTH
cap.set(4, 720)  # CV_CAP_PROP_FRAME_HEIGHT

if cap.isOpened() :
    print("Device loading ok..")
else :
    print("Device loading error..")

while(cap.isOpened()):
    ret,  frame = cap.read()
    print(ret)
    if (ret):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 입력 받은 화면 Gray로 변환
        #find_org_tmp = "./paris_baguette/pstart1.jpg"
        find_org_tmp = "./image/2019052311225227_tmp01.jpg"
        template = cv2.imread(find_org_tmp, 0)
        #template_gray= template.copy();
        #template_gray = cv2.cvtColor(template_gray, cv2.COLOR_BGR2GRAY)  # 입력 받은 화면 Gray로 변환
        w, h = template.shape[::-1]

        print("lot size", w, " | array ", h)

        res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)

        loc = np.where(res >= 0.7)
        print("lot size", len(loc), " | array ", loc,res )
        if (len(loc[1]) > 0):

            for pt in zip(*loc[::-1]):
                cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), thickness=4)
                print("FIND SAME IMAGE MachingError======== ")
                filename = str(time.strftime("%Y_%m_%d_%H_%M")) + '@@find.jpg'
                resized_frame = cv2.resize(frame, (1280, 720))
                cv2.imwrite(filename, resized_frame)
                break


        cv2.imshow('MAIN_WIN', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break





cap.release()
cv2.destroyAllWindows()