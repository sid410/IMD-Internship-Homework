#Live カメラの保存について
import cv2

#Live camera
cap=cv2.VideoCapture(0)
#ビデオの幅を 640 ピクセルに設定します
cap.set(3,640)
#ビデオの高さを 480 ピクセルに設定します
cap.set(4,480)
#カメラの明るさを 100 に設定します
cap.set(10,100)

#ここからは増加内容
#ビデオエンコード形式を定義し、VideoWriter を作成する
#エンコード形式の選択 (XVID、MJPG、MP4V)
fourcc = cv2.VideoWriter_fourcc(*"XVID")
#AVIファイルとして保存
out = cv2.VideoWriter("output.avi", fourcc, 20.0, (640, 480))
while True:
    success, img = cap.read()
    if not success:
        break
     #ビデオファイルの書き込み
    out.write(img)
    #ライブビデオを表示する
    cv2.imshow("video", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
out.release()
cv2.destroyAllWindows()
