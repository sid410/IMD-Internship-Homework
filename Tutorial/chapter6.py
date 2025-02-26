import cv2
import numpy as np

path = "Resources/cards.jpg"
img = cv2.imread(path)

#幅50~100,高さ100~400までの部分を切り取る。
roi = img[50:200,100:400]

cv2.imshow("kirinuki",roi)
cv2.waitKey(0)






