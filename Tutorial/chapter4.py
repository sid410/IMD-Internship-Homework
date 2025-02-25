import cv2
import numpy as np



img = cv2.imread("Resources/land.jpg")

img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_canny = cv2.Canny(img,120,200)

cv2.imshow("land",img_canny)


cv2.waitKey(0)
cv2.destroyAllwindows()













