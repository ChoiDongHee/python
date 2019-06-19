import cv2
import numpy as np
from matplotlib import pyplot as plt


class compareImg:
    def __init__(self):
        pass

    def readImg(self, filepath):
        img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
        # cv2.namedWindow("root", cv2.WINDOW_NORMAL) # window 생성
        # cv2.imshow("root", img) # window에 이미지 띄우기
        # cv2.waitKey(5000) # 5초 기다림. 아무키나 입력되면 대기 종료
        # cv2.destroyAllWindows() # window 제거
        return img

    def diffImg(self, img1, img2):
        # Initiate SIFT detector
        orb = cv2.ORB_create()

        # find the keypoints and descriptors with SIFT
        kp1, des1 = orb.detectAndCompute(img1, None)
        kp2, des2 = orb.detectAndCompute(img2, None)

        # create BFMatcher object
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

        # Match descriptors.
        matches = bf.match(des1, des2)

        # Sort them in the order of their distance.
        matches = sorted(matches, key=lambda x: x.distance)

        # BFMatcher with default params
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1, des2, k=2)

        # Apply ratio test
        good = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good.append([m])


        # Draw first 10 matches.
        knn_image = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good, None, flags=2)
        plt.imshow(knn_image)
        plt.show()

    def run(self):
        # 이미지 파일 경로 설정
        filepath1 = "./img/org.jpg"
        filepath2 = "./img/tmp.jpg"

        # 이미지 객체 가져옴
        img1 = self.readImg(filepath1)
        img2 = self.readImg(filepath2)

        # 2개의 이미지 비교
        self.diffImg(img1, img2)


if __name__ == '__main__':
    cImg = compareImg()
    cImg.run()
