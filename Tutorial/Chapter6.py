import cv2
import numpy as np

img=cv2.imread("Resources/lena.png")

imgHor=np.hstack((img,img))
imgver=np.vstack((img,img))
imggray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)


cv2.imshow("Horizontal",imgHor)
cv2.imshow("Vertical",imgver)
cv2.imwrite("Horizontal.png",imgHor)
cv2.imwrite("Vertical.png",imgver)


cv2.waitKey(0)
