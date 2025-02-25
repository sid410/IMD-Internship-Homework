import cv2

import numpy as np

img = cv2.imread("Resources/book.jpg")

#画像のサイズを取得
#h,w = img.shape[:2]

#画像のサイズを2倍にする
result = cv2.resize(img,None,fx=2,fy=2)

cv2.imread("Image",result)

#cv2.waitKey(0)

