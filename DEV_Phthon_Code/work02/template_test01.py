import cv2
import numpy as np
from matplotlib import pyplot as plt

filepath1 = "./targetImage/TV.1559205398.0657294.jpg"
filepath2 = "./targetImage/TV.1559205398.0657294_tmp.jpg"

img = cv2.imread(filepath1,0)

template = cv2.imread(filepath2,0)
w, h = template.shape[::-1]

method = eval('cv2.TM_CCORR')

# Apply template Matching
res = cv2.matchTemplate(img,template,cv2.TM_CCOEFF_NORMED)
threshold = 0.8

print(res)

loc = np.where(res >= threshold)

print(loc)

for pt in zip(*loc[::-1]):
    cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
    resized_frame = cv2.resize(img, (1280, 720))
    cv2.imwrite("ccmatchTemplate1.jpg",resized_frame)
    #cv2.imshow('frame_gray', img)  # Gray 화면 출력
    #cv2.imshow('frame_template', template)  # Gray 화면 출력


cv2.destroyAllWindows()
