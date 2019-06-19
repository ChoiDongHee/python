import numpy as np
import cv2
import time
import matplotlib.pyplot as plt



cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('haarcascade_frontface.xml')

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    cam = cv2.VideoCapture(0)
    cap.set(3, 460)  # CV_CAP_PROP_FRAME_WIDTH
    cap.set(4, 225)  # CV_CAP_PROP_FRAME_HEIGHT

    # 얼굴 인식 캐스케이드 파일 읽는다

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # for (x, y, w, h) in faces:
    #     cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Display the resulting frame
    cv2.imshow('my frame',frame)

    if cv2.waitKey(1) == ord('q'):
        print("====================")
        break


cap.release()
cv2.destroyAllWindows()








