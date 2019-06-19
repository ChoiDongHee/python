import cv2
import numpy as np
import time
import datetime
from datetime import datetime

import matplotlib.pyplot as plt
import threading
import requests
import http.client

def smartPush(userSaid):
    conn = http.client.HTTPSConnection("spisdev.paran.com")
    payload = "{\n  \"said\": [\n    \""+userSaid+"\"\n  ]\n}\n"
    print(payload)
    headers = {
        'content-type': "application/json",
        'x-auth-token': "1e4dfe44-d7e9-dce2-1d5a-0a46-6ad3-5b57-3ab9-05a3-273f-38a76abddc3ead3d4c20",
        'cache-control': "no-cache",
        'postman-token': "ac070378-ba5b-ffe5-34cb-28ad12a816c9"
    }

    conn.request("POST", "/sprtm/message/send/201810311011", payload, headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))

# ===============  utill end ======================
def getNowTime():
    now = time.localtime()
    s = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    return s

# ===============  utill end   ======================


# === test File save =========
def saveimage(frame):
    dt = getNowTime()
    nowfile =  './resource/TV.'+str((time.time()+300) )+'.jpg'
    #rzTmp = cv2.resize(frame, (100, 75))
    rzTmp = cv2.resize(frame, (1280, 720))
    cv2.imwrite(nowfile, rzTmp)

def saveMatchTemplateimage(frame):

    global said

    nowfile =  './tmpImage/FIND_IMG_THREAD.'+ str((time.time()+300) )+'.jpg'
    rzTmp = cv2.resize(frame, (1280, 720))
    cv2.imwrite(nowfile, rzTmp)

    #smartPush(said)

    image = cv2.imread(nowfile, cv2.IMREAD_UNCHANGED )
    windowsName = "SNAKE EYES"
    imageResizeTmp = cv2.resize(image, (700, 500))
    cv2.imshow(windowsName, imageResizeTmp)
    cv2.waitKey(0)



# ===============  openCv MatchTemplate Main start ======================
def getMatchTemplate(capOrgFrame):

    global findTemplateThumbnail
    global imageBufferIdx
    global globalMainImage
    global findTemplateThumbnailImageListArray
    try:
        for findImageThumbnailImage in findTemplateThumbnailImageListArray:
            w, h = findImageThumbnailImage.shape[::-1]
            res = cv2.matchTemplate(capOrgFrame, findImageThumbnailImage, cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= 0.9)
            if (len(loc[1]) > 0):
                for pt in zip(*loc[::-1]):
                    cv2.rectangle(capOrgFrame, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), thickness=4)
                    saveMatchTemplateimage(capOrgFrame)
                    break
    except:
        time.sleep(loopSleepTime)

# 버퍼에 들어온 이미지를 돌아가 면서 입력 한다.
def setCAPImagelist(frame):
    #====================================================
    #saveimage(frame)
    # ====================================================
    getMatchTemplate(frame.copy())


# ===============  start Main ======================
if __name__ == '__main__':


    # global 변수
    said ="TT181220011"
    iswork = 0
    lock = threading.Lock()
    globalMainImage = [] #이미지 담을 array
    imageBufferIdx = 0   #이미지 배열 idx
    loopSleepTime = 0.1  #이미지 캡처 sleep time
    arrayRang = 1000 # 배열의 큐 크기를 확인 한다.
    findTemplateThumbnailImageListArray = []
    ThumbnailImageListArray = []

    #ThumbnailImageListArray.append("./targetImage/TV.1559205389.847259_tmp.jpg") #찾을 파일 리스트 현재는 단일
    #ThumbnailImageListArray.append("./targetImage/TV.1558920176.9985843_tmp.jpg")  # 찾을 파일 리스트 현재는 단일
    #ThumbnailImageListArray.append("./targetImage/TV.1558925810.655175_tmp.jpg")  # 찾을 파일 리스트 현재는 단일
    #ThumbnailImageListArray.append("./targetImage/TV.1558925821.8908176_tmp.jpg")  # 찾을 파일 리스트 현재는 단일

    ThumbnailImageListArray.append("./targetImage/TV.1559205398.0657294_tmp.jpg")  # 찾을 파일 리스트 현재는 단일
    ThumbnailImageListArray.append("./targetImage/TV.1559205389.847259_tmp.jpg")  # 찾을 파일 리스트 현재는 단일




    ##
    defalutImageBaseLogo = cv2.imread("./targetImage/snakeeyes.jpg", cv2.IMREAD_UNCHANGED)
    defalutImageBaseLogoWindowName = "SNAKE EYES"
    idefalutImageBaseLogoImageLoad = cv2.resize(defalutImageBaseLogo, (700, 500))
    cv2.imshow(defalutImageBaseLogoWindowName, idefalutImageBaseLogoImageLoad)  # logo  컬러 화면 출력
    ##
    i=1 ;
    for findImageThumbnailImage in ThumbnailImageListArray:
        findTemplateThumbnailImageListArray.append(cv2.imread(findImageThumbnailImage, 0))
        print(findImageThumbnailImage)
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
        print("version..:", "v32")
        # cap get image Cap start =============== loop start ======================
        loopCount = 0
        while (cap.isOpened()):
            ret, frame = cap.read()  # Read 결과와 frame
            if (ret):
                #print("globalMainImage size : " ,len(globalMainImage))
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 입력 받은 화면 Gray로 변환

                time.sleep(0.05)
                my_thread= threading.Thread(
                     target=setCAPImagelist, args=(gray.copy(),))
                my_thread.start()

                cv2.imshow('Main Channel', frame)  # main창 컬러 화면 출력

                #
                for idx in range(0,len(findTemplateThumbnailImageListArray)):
                     windowname = str(idx)+"_target"
                     imageResizeTmp = cv2.resize(findTemplateThumbnailImageListArray[idx], (320, 240))
                     cv2.imshow(windowname, imageResizeTmp)  # 컬러 화면 출력

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
