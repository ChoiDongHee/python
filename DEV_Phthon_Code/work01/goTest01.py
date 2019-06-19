import numpy as np
import cv2
import time


cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    cam.set(3, 1280)  # CV_CAP_PROP_FRAME_WIDTH
    cam.set(4, 720)  # CV_CAP_PROP_FRAME_HEIGHT


    # 얼굴 인식 캐스케이드 파일 읽는다
    face_cascade = cv2.CascadeClassifier('haarcascade_frontface.xml')

    while True:

        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)


        # 인식된 얼굴 갯수를 출력f
        print(len(faces))

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)


         # Display the resulting frame
        cv2.imshow('my frame',frame)


        if cv2.waitKey(1) != 255:
            break;

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()






