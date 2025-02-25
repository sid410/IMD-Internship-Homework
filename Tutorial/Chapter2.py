import cv2
#Python terminal　中にnumpy backageをダウンロード
# pip install numpy　in Python terminal (CMD)or(PowerShell)
#numpy を導入npをコマンド設定
import numpy as np
print("ok")

img=cv2.imread("Resources/lena.png")
#5x5 行列 (カーネル)、すべての要素は 1、データ型は np.uint8 です。
kernal=np.ones((5,5),np.uint8)

#カラー画像をグレースケール画像に変換する
# img->オリジナルの BGR カラー画像
# cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) → カラー形式を変換
# cv2.COLOR_BGR2GRAY → BGR をグレースケールに変換
imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#ガウスぼかしは画像を処理し、主にノイズ低減、スムージング、ディテールの除去に使用されます。
imgBlur=cv2.GaussianBlur(imgGray,(7,7),0)
#キャニーエッジ検出（Canny Edge Detection）
imgCanny=cv2.Canny(img,100,100)
#Sample 2
imgCannySample2=cv2.Canny(img,150,200)
#エッジを拡張して、オブジェクトの輪郭をより見やすくします。
imgDialation=cv2.dilate(imgCanny,None,iterations=2)
#Sample2
imgDialationSample2=cv2.dilate(imgCannySample2,kernal,iterations=2)
#Sample3
imgDialationSample3=cv2.dilate(imgCanny,None,iterations=10)
#オブジェクトの輪郭を細くする
imgErroded=cv2.erode(imgDialation,kernal,iterations=1)
cv2.imshow("orgin",img)
cv2.imshow("gray Image",imgGray)
cv2.imshow("Blur Image",imgBlur)
cv2.imshow("Canny",imgCanny)
cv2.imshow("CannySample2",imgCannySample2)
cv2.imshow("Dialation",imgDialation)
cv2.imshow("Dialation sample2",imgDialation)
cv2.imshow("Dialation Sample3",imgDialationSample3)
cv2.imshow("Erroded",imgErroded)
cv2.waitKey(0)
#保存する
cv2.imwrite("orgin.png",img)
cv2.imwrite("gray Image.png",imgGray)
cv2.imwrite("Blur Image.png",imgBlur)
cv2.imwrite("Canny.png",imgCanny)
cv2.imwrite("CannySample2.png",imgCannySample2)
cv2.imwrite("Dialation.png",imgDialation)
cv2.imwrite("Dialation sample2.png",imgDialation)
cv2.imwrite("Dialation Sample3.png",imgDialationSample3)
cv2.imwrite("Erroded.png",imgErroded)
cv2.waitKey(0)
cv2.destroyAllWindows()