import cv2
import numpy as np

img = np.zeros((512,512,3),np.uint8)
#print(img.shape)
#一部を青に
#print(img)
#img[200:300,300:500]= 255,0,0

#途中まで線
#cv2.line(img,(0,0),(300,300),(255,255,0),3)

#最後まで線
cv2.line(img,(0,0),(img.shape[1],img.shape[0]),(255,255,0),3)
#箱
cv2.rectangle(img,(0,0),(250,350),(0,0,255),cv2.FILLED)
#円
cv2.circle(img,(400,50),30,(255,255,0),5)
#テキストを書く
cv2.putText(img," OPENCV ",(300,300),cv2.FONT_HERSHEY_COMPLEX,1,(0,150,0),1)

cv2.imshow("Image",img)

cv2.waitKey(0)