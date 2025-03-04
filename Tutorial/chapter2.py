import cv2
import numpy as np

def stackImages(scale,imgArray):
    rows=len(imgArray)
    cols=len(imgArray[0])
    rowsAvailble=isinstance(imgArray[0],list)
    width=imgArray[0][0].shape[1]
    height=imgArray[0][0].shape[0]
    if rowsAvailble:
        for x in range(0,rows):
            for y in range(0,cols):
                if imgArray[x][y].shape[:2]==imgArray[0][0].shape[:2]:
                    imgArray[x][y]=cv2.resize(imgArray[x][y],(0,0),None,scale,scale)
                else:
                    imgArray[x][y]=cv2.resize(imgArray[x][y],(imgArray[0][0].shape[1],imgArray[0][0].shape[0]),None,scale,scale)
                if len(imgArray[x][y].shape)==2:imgArray[x][y]=cv2.cvtColor(imgArray[x][y],cv2.COLOR_GRAY2BGR)
        imageBlank=np.zeros((height,width,3),np.uint8)
        hor=[imageBlank]*rows
        # hor_con=[imageBlank]*rows
        for x in range(0,rows):
            hor[x]=np.hstack(imgArray[x])
        ver=np.vstack(hor)
    else:
        for x in range(0,rows):
            if imgArray[x].shape[:2]==imgArray[0].shape[:2]:
                imgArray[x]=cv2.resize(imgArray[x],(0,0),None,scale,scale)
            else:
                imgArray[x]=cv2.resize(imgArray[x],(imgArray[0].shape[1],imgArray[0].shape[0]),None,scale,scale)
            if len(imgArray[x].shape)==2:imgArray[x]=cv2.cvtColor(imgArray[x],cv2.COLOR_GRAY2BGR)
        hor=np.hstack(imgArray)
        ver=hor
    return ver

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

imgBlank=np.zeros_like(img)

imgStack=stackImages(0.6,([img,imgGray,imgBlur],[imgCanny,imgDialation,imgEroded]))
cv2.imshow("Stacked about original,gray,blur,canny,dialation,eroded",imgStack)
# cv2.imshow("Gray Image",imgGray)
# cv2.imshow("Blur Image",imgBlur)
# cv2.imshow("Canny Image",imgCanny)
# cv2.imshow("Dialation Image",imgDialation)
# cv2.imshow("Eroded Image",imgEroded)
cv2.waitKey(0)