import cv2
import numpy as np
import time
import datetime
from datetime import datetime

import matplotlib.pyplot as plt
import threading



# ===============  utill end ======================
def getNowTime():
    now = time.localtime()
    s = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    return s
def Loog(str):
    myThreadCount = threading.active_count()
    print("Log (%d)(%s) : %s || %s \r\n" % (myThreadCount,threading.currentThread().getName(), getNowTime(),str))
def getNowTime():
    now = time.localtime()
    s = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    return s

# 초기 세팅 배열에 담듣다 ------
def setDefaultImagelist(userArraySize):
    global globalMainImage

    try:
        templateDefaultImage = cv2.imread(defalutStartImage, 0)
        for i in range(userArraySize):
            globalMainImage.append(templateDefaultImage)
            print("init start : ", i )
    except:
        print("setDefaultImagelist list err")


# ===============  utill end   ======================


# === test File save =========
def saveimage(frame):
    dt = getNowTime()
    nowfile =  './resource/CAP_IMG_THREAD.'+str((time.time()+300) )+'.jpg'
    #rzTmp = cv2.resize(frame, (100, 75))
    rzTmp = cv2.resize(frame, (1280, 720))
    cv2.imwrite(nowfile, rzTmp)

def saveMatchTemplateimage(frame):
    dt = getNowTime()
    nowfile =  './tmpImage/TH_IMG_THREAD.'+str((time.time()+300) )+'.jpg'
    rzTmp = cv2.resize(frame, (1280, 720))
    cv2.imwrite(nowfile, rzTmp)

# ===============  openCv MatchTemplate Main start ======================
def getMatchTemplate(keyIdx):

    global findTemplateThumbnail
    global imageBufferIdx
    global globalMainImage
    global findTemplateThumbnailImage

    try:
        print("FIND$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ ARRAY :" , keyIdx)
        w, h = findTemplateThumbnailImage.shape[::-1]

        saveMatchTemplateimage(globalMainImage[keyIdx])

        tcapOrgFrame = globalMainImage[keyIdx] #for i=1 부터 루프 됨
        capOrgFrame = tcapOrgFrame.copy();


        res = cv2.matchTemplate(capOrgFrame, findTemplateThumbnailImage, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= 0.75)

        if (len(loc[1]) > 0):
            for pt in zip(*loc[::-1]):
                cv2.rectangle(capOrgFrame, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), thickness=4)
                print(">>>>>>>>>>  FIND SAME IMAGE ")
                findFileName = str(time.strftime("%Y_%m_%d_%H_%M")) + '@@find.jpg'
                resized_frame = cv2.resize(capOrgFrame, (1280, 720))
                cv2.imwrite(findFileName, resized_frame)
                time.sleep(loopSleepTime)

        time.sleep(loopSleepTime)
    except:
        time.sleep(loopSleepTime)

# 버퍼에 들어온 이미지를 돌아가 면서 입력 한다.
def setCAPImagelist(frame):
    global imageBufferIdx
    global globalMainImage
    arraySize = len(globalMainImage)-1

    print("=========================>>",imageBufferIdx , arraySize)

    saveimage(frame)
    getMatchTemplate(imageBufferIdx)
    cfrmae = frame.copy()

    if (imageBufferIdx >= arraySize):
        globalMainImage[imageBufferIdx] = cfrmae  # 이미지를 배열에 담는다.
        imageBufferIdx = 0
    else:
        globalMainImage[imageBufferIdx] = cfrmae  # 이미지를 배열에 담는다.
        imageBufferIdx = imageBufferIdx + 1


        #saveimage(globalMainImage[imageBufferIdx])



# ===============  openCv MatchTemplate Main end ======================

# ===============  start Main ======================
if __name__ == '__main__':


    # global 변수
    iswork = 0
    lock = threading.Lock()
    globalMainImage = [] #이미지 담을 array
    imageBufferIdx = 0   #이미지 배열 idx
    loopSleepTime = 0.1  #이미지 캡처 sleep time
    arrayRang = 1000 # 배열의 큐 크기를 확인 한다.
    findTemplateThumbnail = "./targetImage/bigboy.png"  #찾을 파일 리스트 현재는 단일
    defalutStartImage = './targetImage/defalut_start.jpg'
    #이미지 배열 초기화 진행
    setDefaultImagelist(arrayRang); # 초이 이미지를 넣어서 오류나지 않게 처리한다.

    findTemplateThumbnailImage = cv2.imread(findTemplateThumbnail, 0)


    #전처리 END ========================
    cap = cv2.VideoCapture(0)
    #cap.set(3, 320)  # CV_CAP_PROP_FRAME_WIDTH
    #cap.set(4, 180)  # CV_CAP_PROP_FRAME_HEIGHT
    cap.set(3, 1280)  # CV_CAP_PROP_FRAME_WIDTH
    cap.set(4, 720)  # CV_CAP_PROP_FRAME_HEIGHT
    #cap.set(5,0)  # CV_CAP_PROP_FPSq


    if cap.isOpened() :
        # cap get image Cap start =============== isOpened start ======================
        fps = int(cap.get(5))
        print("Device loading ok..:",fps)
        # cap get image Cap start =============== loop start ======================
        loopCount = 0
        while (cap.isOpened()):
            ret, frame = cap.read()  # Read 결과와 frame
            if (ret):
                #print("globalMainImage size : " ,len(globalMainImage))
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 입력 받은 화면 Gray로 변환
                 #큐에 gray 이미지 파일을 넣는다#
                #setCAPImagelist(gray)
                time.sleep(0.05)
                my_thread= threading.Thread(
                     target=setCAPImagelist, args=(gray.copy(),))
                my_thread.start()

                #saveimage(gray)

                # print("===>",loopCount, imageBufferIdx)

                 # my_thread= threading.Thread(
                 #     target=getMatchTemplate, args=(imageBufferIdx,))
                 # my_thread.start()

                #cv2.imshow('frame_color', frame)  # 컬러 화면 출력
                #cv2.imshow('frame_gray', gray)  # Gray 화면 출력
                if cv2.waitKey(1) == ord('q'):
                    break
            else:
                print("============frame = cap.read() Error==================")
                break


        # cap get image Cap start =============== loop end ======================
        # cap get image Cap start =============== isOpened end ======================
    else :
        print("Device loading error..")


cap.release()
cv2.destroyAllWindows()


# ===============  start Main ======================

#                myThread = threading.Thread(target=getMatchTemplate, args=(1,))
#                 myThread.start()
#                 myThread2 = threading.Thread(target=getMatchTemplate, args=(1,))
#                 myThread2.start()
#                 myThread3 = threading.Thread(target=getMatchTemplate, args=(1,))
#                 myThread3.start()
#                 myThread4 = threading.Thread(target=getMatchTemplate, args=(1,))
#                 myThread4.start()
#                 myThread5 = threading.Thread(target=getMatchTemplate, args=(1,))
#                 myThread5.start()