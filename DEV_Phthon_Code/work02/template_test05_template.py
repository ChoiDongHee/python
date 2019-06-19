import numpy as np
import cv2

# filepath1 = "./paris_baguette/end.png"
# filepath2 = "./paris_baguette/end_org.png"

filepath1 = "./resource/111.jpg"
filepath2 = "./targetImage/bigboy.png"


img = cv2.imread(filepath1)
#imgray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
imgray = img
h, w = imgray.shape[:2]

print("w",w ," | h ", h)

templ = cv2.imread(filepath2, 0)
templ_h, templ_w = templ.shape[:2]


res = cv2.matchTemplate(imgray, templ, cv2.TM_CCOEFF_NORMED)
loc = np.where(res >= 0.5)
print("lot size",len(loc) ," | array ", loc)
if(len(loc[1]) > 0):
    print("FIND SAME IMAGE matchTemplate ")
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img, pt, (pt[0] + templ_w, pt[1] + templ_h), (0, 0, 255),thickness=4)
        print(">>",pt)
        break


cv2.imshow("res", img)
cv2.waitKey(0)


