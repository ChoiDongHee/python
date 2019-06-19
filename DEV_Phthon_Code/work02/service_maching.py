import cv2
import numpy as np
import time
import threading

filepath2 = "./image/tmp01_1.jpg"

fileSize = [320,180]
fileArray = [1,2,3,4,5]
keyLoop = 0
lock = threading.Lock()
oldFileName = 0

def matchTemplate(matchTemplate):
     #400*225 , 100*56
    global keyLoop
    global fileArray
    global fileSize
    global lock
    global oldFileName
    global filepath2

    lock.acquire()
    try:
        localKeyLoop = keyLoop
        if keyLoop > 0 and keyLoop < len(fileArray):
            localKeyLoop = localKeyLoop - 1
        elif keyLoop == 0:
            localKeyLoop = len(fileArray) - 1
        elif localKeyLoop < 0:
            localKeyLoop = 0
        filepath1 = oldFileName

        print(filepath1)

        img = cv2.imread(filepath1)
        imgray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        h, w = imgray.shape[:2]

        print("w", w, " | h ", h)

        templ = cv2.imread(filepath2, cv2.IMREAD_GRAYSCALE)
        templ_h, templ_w = templ.shape[:2]
        res = cv2.matchTemplate(imgray, templ, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= 0.5)
        #print("lot size", len(loc), " | array ", loc)
        if (len(loc[1]) > 0):
            print("FIND SAME IMAGE matchTemplate ")
            for pt in zip(*loc[::-1]):
                cv2.rectangle(img, pt, (pt[0] + templ_w, pt[1] + templ_h), (0, 0, 255), thickness=4)
                print(">>", pt)
                matchTemplateFindimgFileSave(img)
                break
    finally:
         lock.release()
    print(threading.currentThread().getName() + ' Synchronized  :', localKeyLoop)

def matchTemplateFindimgFileSave(frame):
    global oldFileName
    global fileSize
    filename =  "Find_"+oldFileName+'.jpg'
    resized_frame = cv2.resize(frame, (fileSize[0], fileSize[1]))
    cv2.imwrite(filename, resized_frame)

def imgFileSave(frame):
     #400*225 , 100*56
    global keyLoop
    global fileArray
    global fileSize
    global lock
    global oldFileName

    nowFileName =  str(time.strftime("%Y_%m_%d_%H_%M-"))
    if keyLoop == len(fileArray) :
        keyLoop = 0
        print("array size same")
    if oldFileName != nowFileName:
        keyLoop = 0
        print("filename is not machage1")
    filename =  nowFileName + str(fileArray[keyLoop])+ '.jpg'
    resized_frame = cv2.resize(frame, (fileSize[0], fileSize[1]))
    cv2.imwrite(filename, resized_frame)
    keyLoop  = keyLoop + 1
    oldFileName= filename
    print("Image Capture Loading Success.....",keyLoop ,oldFileName , nowFileName)

    return oldFileName





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
        saveFileName= imgFileSave(frame)
        matchTemplate(saveFileName)
        #cv2.imshow('frame_color', frame)    # 컬러 화면 출력
        cv2.imshow('frame_gray', gray)    # Gray 화면 출력
        if cv2.waitKey(1) == ord('q'):
            break


cap.release()
cv2.destroyAllWindows()
