import numpy as np
import cv2
import time
import matplotlib.pyplot as plt

def templateImage(org ,tmp):
    img_rgb = cv2.imread(org, 0)
    img_gray =  org
    #img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(tmp, 0)
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
    print(count)

while True:
    filepath1 = "./tmpImage/TH_IMG_THREAD.1558687157.007457.jpg"
    filepath2 = "./targetImage/bigboy.png"
    templateImage(filepath1,filepath2)