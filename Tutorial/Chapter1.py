

#先ず　packageを導入する
import cv2
print("have imported")
#図を表示
img=cv2.imread(r"Resources/lena.png")
cv2.imshow("output",img)
#Outputの時間(0)はずっと表示　1000は1秒表示 通常、待機時間を示すために他のコマンドと一緒に使用されます。
cv2.waitKey(0)



#この部分はvideoの表示
cap=cv2.VideoCapture("Resources/test_video.mp4")
#Qキーが止まるまで無限ループコマンド
while True:
    success,img=cap.read()
    cv2.imshow("video",img)
    #「q」を押すと、while ループを終了してウィンドウを閉じます。
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
