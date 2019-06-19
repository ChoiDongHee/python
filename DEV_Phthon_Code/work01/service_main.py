import cv2
import numpy as np
import pytesseract

cap = cv2.VideoCapture(0)
cap.set(3, 430)  # CV_CAP_PROP_FRAME_WIDTH
cap.set(4, 225)  # CV_CAP_PROP_FRAME_HEIGHT
# cam.set(5, 0)  # CV_CAP_PROP_FPSq
print("VideoCapture Loading Success.....")
print('width :%d, height : %d' % (cap.get(3), cap.get(4)))


while(True):
    print("Start engin ...")
    ret, frame = cap.read()    # Read 결과와 frame
    print(ret);
    if(ret) :
        gray = cv2.cvtColor(frame,  cv2.COLOR_BGR2GRAY)    # 입력 받은 화면 Gray로 변환
        print(pytesseract.image_to_string(gray))
        #cv2.imshow('frame_color', frame)    # 컬러 화면 출력
        cv2.imshow('frame_gray', gray)    # Gray 화면 출력
        if cv2.waitKey(1) == ord('q'):
            break


cap.release()
cv2.destroyAllWindows()
