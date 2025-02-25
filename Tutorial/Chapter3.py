import cv2
import numpy as np
print("ok")

img=cv2.imread("Resources/lambo.PNG")
#このコード行は、画像の寸法情報、つまり (高さ、幅、チャネル) を表示するために使用されます。 チャネル=3 カラー　 チャネル==1 Grayscale
print(img.shape)
#画像のサイズを幅 300 ピクセル、高さ 200 ピクセルに変更します。
imgResize=cv2.resize(img,(300,200))
print(imgResize.shape)
#元の拡大縮小された画像
imgcropped=imgResize[0:200,200:500]
cv2.imshow("Cropped",imgcropped)
cv2.imshow("Image",img)
cv2.imshow("Resize",imgResize)
#保存
cv2.imwrite("Before the Change.png",img)
cv2.imwrite("Resize.png",imgResize)
cv2.imwrite("Cropped.png",imgcropped)
cv2.waitKey(0)
#########次の章では、時間の理由についてはコメントを追加しません。