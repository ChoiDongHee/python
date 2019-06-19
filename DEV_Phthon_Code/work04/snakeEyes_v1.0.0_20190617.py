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

def getNowTimePrint():
    now = time.localtime()
    s = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    return s

def draw_text_bg(img):


    return img
# ===============  utill end   ======================


# === test File save =========
def saveimage(frame):
    dt = getNowTime()
    nowfile =  './resource/TV.'+str((time.time()+300) )+'.jpg'
    #rzTmp = cv2.resize(frame, (100, 75))
    rzTmp = cv2.resize(frame, (1280, 720))
    cv2.imwrite(nowfile, rzTmp)

def saveimage2(fileName, frame):
    dt = getNowTime()
    nowfile =  './resource/'+fileName+str((time.time()) )+'.jpg'
    #rzTmp = cv2.resize(frame, (100, 75))
    rzTmp = cv2.resize(frame, (1280, 720))
    cv2.imwrite(nowfile, rzTmp)


def saveMatchTemplateimage(frame,findImageThumbnailImagePath):

    global said
    global cv2
    global StateManager
    global immageSkipTime

    #현재 시간을 구해 줌
    strTime = str((time.time()))


    #특정 시간 동안 찾으면 중복 발솔을 제어 한다 .초기 설정으로 NOT_FOUND 문자 입력
    for searchFimePath in StateManager.keys():

        if searchFimePath == findImageThumbnailImagePath:
            if(StateManager[searchFimePath] in  "NOT_FOUND"):
                StateManager[searchFimePath] = strTime

                #파일을 찾았으므로 tmpImage 파일에 저장하고
                nowfile = './tmpImage/FIND_IMG_THREAD.' + str((time.time() )) + '.jpg'
                rzTmp = cv2.resize(frame, (1280, 720))
                cv2.imwrite(nowfile, rzTmp)

                # smartPush(said)

                # 모니터링 snake eyes 화면에 출력 한다.
                strTimePrint = getNowTimePrint()

                frame = cv2.rectangle(frame, (0, 80), (200, 110), (0, 0, 0), -1)
                #cv2.rectangle(frame, (0,0), (0,300), (255, 0, 0), thickness)
                cv2.putText(frame, strTimePrint, (0, 100), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.5, (255, 255, 255))

                windowsName = "SNAKE EYES"
                # imageResizeTmp = cv2.resize(image, (1280, 720))
                cv2.imshow(windowsName, frame)
                cv2.waitKey(0)
                print("Same Image Frame !!")
            elif( float(StateManager.get(searchFimePath)) < (float(time.time()) - immageSkipTime) ):
                print(float(StateManager.get(searchFimePath)) ,"||++++||", time.time()  )
                StateManager[searchFimePath] = "NOT_FOUND"
                print("Same Image not Time skip!!")
            else:
                print("Same Image Skip!! Else....")

            print("Okay")
        else:
            print("None")



# ===============  openCv MatchTemplate Main start ======================
def getMatchTemplate(capOrgFrameCopy):

    global ThumbnailImageDic
    global cv2

    try:
        icount =1;

        for findImagePath , findImageThumbnailImage in ThumbnailImageDic.items():
            res = cv2.matchTemplate(capOrgFrameCopy, findImageThumbnailImage, cv2.TM_CCOEFF_NORMED)
            w, h = findImageThumbnailImage.shape[::-1]
            loc = np.where(res >= 0.9)
            if (len(loc[1]) > 0):
                for pt in zip(*loc[::-1]):
                    cv2.rectangle(capOrgFrameCopy, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), thickness=4)
                    saveMatchTemplateimage(capOrgFrameCopy,findImagePath)
                    break
    except Exception as ex:  # 에러 종류
        print('에러가 발생 했습니다', ex)  # ex는 발생한 에러의 이름을 받아오는 변수
        icount = icount + 1
        time.sleep(loopSleepTime)


# ===============  start Main ======================
if __name__ == '__main__':


    # global 변수
    said ="TT181220011"
    iswork = 0
    lock = threading.Lock()
    globalMainImage = [] #이미지 담을 array
    imageBufferIdx = 0   #이미지 배열 idx
    loopSleepTime = 0.1  #이미지 캡처 sleep time
    immageSkipTime = 5

    # 찾을려고 하는 이미지 PATH를 DIC Key에 등록 한다.
    ThumbnailImageDic ={}
    ThumbnailImageDic["./targetImage/TV.1558920153.4942398_tmp.jpg"] = "" #찾을 파일 리스트 현재는 단일
    ThumbnailImageDic["./targetImage/TV.1558920176.9985843_tmp.jpg"] = ""   # 찾을 파일 리스트 현재는 단일
    ThumbnailImageDic["./targetImage/TV.1558925810.655175_tmp.jpg"]  = ""  # 찾을 파일 리스트 현재는 단일
    ThumbnailImageDic["./targetImage/TV.1558925821.8908176_tmp.jpg"] = ""   # 찾을 파일 리스트 현재는 단일



    #찾을려고 하는 이미지 중 1번 찾으면 다시 skip하도록 처리
    StateManager = {}
    for findImageStete in ThumbnailImageDic.keys():
        StateManager[findImageStete] ="NOT_FOUND"

    ## 타켓 이미지 통합 jpg 를 출력 한다.
    sumDetectListImage = cv2.imread("./targetImage/detect_sum.jpg", 0)
    sumDetectListResizeImage = cv2.resize(sumDetectListImage, (633, 512))
    cv2.imshow("Target template", sumDetectListResizeImage)  # 컬러 화면 출력

    ## SNAKE EYES detecting 창을 출력 한다.q
    defalutImageBaseLogo = cv2.imread("./targetImage/snakeeyes_bg.png", cv2.IMREAD_UNCHANGED)
    defalutImageBaseLogoWindowName = "SNAKE EYES"
    idefalutImageBaseLogoImageLoad = cv2.resize(defalutImageBaseLogo, (1280, 720))
    cv2.imshow(defalutImageBaseLogoWindowName, idefalutImageBaseLogoImageLoad)  # logo  컬러 화면 출력

    ## key에 타켓 이미지 리스트를 담는다.
    for searchFimePath in ThumbnailImageDic.keys():
        targetImageGray = cv2.imread(searchFimePath)
        ThumbnailImageDic[searchFimePath]  = cv2.cvtColor(targetImageGray, cv2.COLOR_BGR2GRAY)  # 입력 받은 화면 Gray로 변환




    ##Vedeo Capture Start  ========================
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)  # CV_CAP_PROP_FRAME_WIDTH
    cap.set(4, 720)  # CV_CAP_PROP_FRAME_HEIGHT


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
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 입력 받은 화면 Gray로 변환

                time.sleep(0.05)
                my_thread = threading.Thread(
                     target=getMatchTemplate, args=(gray.copy(),))
                my_thread.start()

                strTimePrint = getNowTimePrint()
                frame = cv2.rectangle(frame, (0, 80), (200, 110), (0, 0, 0), -1)
                cv2.putText(frame, strTimePrint, (0, 100), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.5, (255, 255, 255))


                cv2.imshow('Main Service Channel', frame)  # main창 컬러 화면 출력

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
