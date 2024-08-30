import cv2

face_cascade = cv2.CascadeClassifier(r"Resources\haarcascade_frontalface_default.xml")
img = cv2.imread(r"Resources\lena.png")
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces =face_cascade.detectMultiScale(img_gray, 1.1, 4)

for (x,y,w,h) in faces:
    cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)

cv2.imshow("Result", img)
cv2.waitKey(0)
cv2.destroyAllWindows()