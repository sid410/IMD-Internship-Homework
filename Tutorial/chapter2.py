import cv2
import numpy as np

img = cv2.imread("Tutorial/Resources/lena.png")
kernel = np.ones((5,5),np.uint8)

##gray
imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
##ぼかし
imgBlur = cv2.GaussianBlur(imgGray,(7,7),0)
##輪郭
imgCanny = cv2.Canny(img,200,200)
##輪郭膨張
imgDialation = cv2.dilate(imgCanny,kernel,iterations=1)
##膨張縮小
imgEroded = cv2.erode(imgDialation,kernel,iterations=1)


cv2.imshow("Gray Image",imgGray)
cv2.imshow("Blur Image",imgBlur)
cv2.imshow("Canny Image",imgCanny)
cv2.imshow("Dialation Image",imgDialation)
cv2.imshow("Eroded Image",imgEroded)
cv2.waitKey(0)