import cv2
import numpy as np
from matplotlib import pyplot as plt

filepath1 = "./img/org01.jpg"
filepath2 = "./img/tmp.jpg"


sift = cv2.xfeatures2d.SIFT_create()


img = cv2.imread(filepath1,0)
img2 = img.copy()
template = cv2.imread(filepath2,0)
w, h = template.shape[::-1]

# All the 6 methods for comparison in a list
methods = ['cv2.TM_CCOEFF','cv2.TM_CCORR']

for meth in methods:
    img = img2.copy()
    method = eval(meth)

    # Apply template Matching
    res = cv2.matchTemplate(img,template,method)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc

    print("top_left============================")
    print(top_left)
    print("============================")

    bottom_right = (top_left[0] + 20, top_left[1] + 20)

    cv2.rectangle(img,top_left, bottom_right,  (0, 255, 0), 2,5)
    cv2.imshow('my frame', img2)