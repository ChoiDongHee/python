import numpy as np
import cv2
import time

def templateImage(org ,tmp):
    img_rgb = cv2.imread(org)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv.imread('./img/tmp01.jpg', 0)

    w, h = template.shape[::-1]

    res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)

    threshold = 0.8
    loc = np.where(res >= threshold)

    mapped = zip(*loc[::-1])
    mapped = list(mapped)
    count = len(mapped)

    return count


cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    cam = cv2.VideoCapture(0)
    cam.set(3, 1280)  # CV_CAP_PROP_FRAME_WIDTH
    cam.set(4, 720)  # CV_CAP_PROP_FRAME_HEIGHT
    # cam.set(5,0) #CV_CAP_PROP_FPS

    tmpImage = cv2.imread('./img/tmp01.jpg', 0);

    while True:
        ret, frame = cap.read()

        n =   templateImage(frame ,tmpImage )

        if n > 0 :
             filename = str(time.time());
             cv2.imwrite(filename+'.jpg', frame)
             print("====================== 일치 =======================")
        # Display the resulting frame
        cv2.imshow('my frame',frame)

        if cv2.waitKey(1) != 255:
            break;

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()






