import cv2

#学習モデル(顔検出器のロード)
imgface = cv2.CascadeClassifier("Resources/haarcascade_frontalface_default.xml")

img = cv2.imread(r"Resources/lena.png")

if img is None:
    print("error")
else:
    print("yes")
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

#顔検出
faces = imgface.detectMultiScale(gray,1.1,8)

#検出した顔を描画
for (x,y,w,h) in faces:
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)

cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllwindows()





