import numpy as np
import cv2
import time
import matplotlib.pyplot as plt


def templateImage(org ,tmp):
    img_rgb = org

    img_gray =  org
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    #template = cv2.imread(tmp, 0)
    template = cv2.imread('./img/png01.png', 0)

    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)

    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_gray, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

    cv2.imshow('result1', img_gray)
    cv2.imshow('result2', template)

    mapped = zip(*loc[::-1])
    mapped = list(mapped)
    count = len(mapped)
    print(">>")
    print( count )
    return count



cap = cv2.VideoCapture(0)



while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    cam = cv2.VideoCapture(0)
    cap.set(3, 1280)  # CV_CAP_PROP_FRAME_WIDTH
    cap.set(4, 720)  # CV_CAP_PROP_FRAME_HEIGHT
    #cam.set(5,0) #CV_CAP_PROP_FPS

    # 얼굴 인식 캐스케이드 파일 읽는다
    face_cascade = cv2.CascadeClassifier('haarcascade_frontface.xml')

    #cv2.imwrite('messigray.png', frame, params=[cv2.IMWRITE_PNG_COMPRESSION, 0])


    while True:
        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        #print(frame)

        # 인식된 얼굴 갯수를 출력
        #templateImage(gray, './img/tmp01.jpg')

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Display the resulting frame
        cv2.imshow('my frame',frame)

        if cv2.waitKey(1) != 255:
            break;
q




# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()






