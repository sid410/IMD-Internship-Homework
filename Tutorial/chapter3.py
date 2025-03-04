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

img = cv2.imread("/Users/ryosuke371/Documents/GitHub/IMD-Internship-Homework/Tutorial/Resources/lambo.PNG")
print(img.shape)

imgResize = cv2.resize(img,(300,200))
print(imgResize.shape)

imgCropped = img[0:200,200:500]

imgStack=stackImages(0.6,([img,imgResize,imgCropped]))
# cv2.imshow("Image",img)
# cv2.imshow("Image Resize",imgResize)
# cv2.imshow("Image Cropped",imgCropped)
cv2.imshow("Stacked about Original,Resize,Cropped",imgStack)

cv2.waitKey(0)