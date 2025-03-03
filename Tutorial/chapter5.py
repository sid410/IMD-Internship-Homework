#透視変換（指定した領域（カード）をくり抜くような処理）
import cv2
import numpy as np

img = cv2.imread("/Users/ryosuke371/Documents/GitHub/IMD-Internship-Homework/Tutorial/Resources/cards.jpg")
print(img.shape)
width,height = 250,350
pts1 = np.float32([[111,219],[287,188],[154,482],[352,440]])
pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])
matrix = cv2.getPerspectiveTransform(pts1,pts2)
imgOutput = cv2.warpPerspective(img,matrix,(width,height))

cv2.imshow("Image",img)
cv2.imshow("Output",imgOutput)
cv2.waitKey(0)