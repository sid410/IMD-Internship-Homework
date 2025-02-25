import cv2

#Live camera
cap=cv2.VideoCapture(0)
#ビデオの幅を 640 ピクセルに設定します
cap.set(3,640)
#ビデオの高さを 480 ピクセルに設定します
cap.set(4,480)
#カメラの明るさを 100 に設定します
cap.set(10,100)

while True:
    success,img=cap.read()
    cv2.imshow("video",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
