import pyocr
import os
import cv2
import numpy as np
import sys
from PIL import Image

tools = pyocr.get_available_tools()
tool = tools[0]
if len(tools) == 0:
    print("OCR tool is not found.")
    sys.exit(1)
lan = "eng"

#OCRエンジン取得
tools = pyocr.get_available_tools()
tool = tools[0]

#OCRの設定 ※tesseract_layout=6が精度には重要。デフォルトは3
builder = pyocr.builders.TextBuilder(tesseract_layout=6)

file_path = r"/Users/ryosuke371/Desktop/sample_movie.mp4"

#動画読み込み
cap = cv2.VideoCapture(file_path)

# 最初のフレームを読み込む
_, img = cap.read()
# imgは読み込んだフレームのNumpy配列でのピクセル情報(BGR)
# imgのshapeは (高さ, 横幅, 3)

#スライス範囲は高さ:幅
cut_img = img[600:670,50:1050]

kernel = np.array([[ 0, -0.5,  0],
                   [-0.5,  3, -0.5],
                   [ 0, -0.5,  0]])

#画像の前処理
imgHSV=cv2.cvtColor(cut_img,cv2.COLOR_BGR2HSV)
imgBlur = cv2.GaussianBlur(imgHSV,(9,9),0)
imgSharp = cv2.filter2D(imgBlur,-1,kernel)
lower=np.array([0,0,190])
upper=np.array([255,255,255])
imgGray=cv2.inRange(imgSharp,lower,upper)

#前処理したデータをrgbに
img=cv2.cvtColor(imgGray,cv2.COLOR_GRAY2RGB)

# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

edge_img=cv2.Canny(imgGray,60,60)
kernel = np.ones((3,3),np.uint8)
edge_img=cv2.dilate(edge_img,kernel,iterations=3)
cv2.imshow("edge",edge_img)

contours,hierarchy=cv2.findContours(imgGray,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

out=[]
for c in contours:
    if cv2.contourArea(c) > 0:
        out.append(c)
mask = np.ones(edge_img.shape)
for i in range(len(out)):
    cv2.fillConvexPoly(mask, out[i], (0))

cv2.imshow("mask",mask)

mask = np.ones(edge_img.shape)*255
for i in range(len(contours)):
    cv2.fillConvexPoly(mask, contours[i], (0))
mask = cv2.dilate(mask, None, iterations=3)
mask = cv2.erode(mask, None, iterations=3)
mask_stack = np.dstack([mask]*3).astype('float32')
image = (img/255.).astype('float32')
sub_image = cv2.subtract(image, mask_stack)

background_white = np.full_like(img, 255, dtype=np.uint8)  # 真っ白な画像
sub_image = np.where(mask[:, :, None] == 255, background_white, img)

cv2.imshow("Image",sub_image)
cv2.waitKey(0)

# 値を 0-1 の範囲に収める
sub_image = np.clip(sub_image, 0, 1)

# 0-255 にスケール変換して uint8 に変換
sub_image = (sub_image * 255).astype(np.uint8)

#numpy型からimage型に
mask_pil = Image.fromarray(sub_image)

#textを抽出して表示
txt_pyocr = tool.image_to_string(mask_pil , lang='eng', builder=builder)
print('Texto: ',txt_pyocr)





# cv2.imshow("Frame",cut_img)
# cv2.waitKey(0)

# # 横幅
# print(f"width: {cap.get(cv2.CAP_PROP_FRAME_WIDTH)}")
# # width: 600.0

# # 高さ
# print(f"height: {cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}")
# # height: 360.0

# # フレームレート
# print(f"fps: {cap.get(cv2.CAP_PROP_FPS)}")
# # fps: 30.0

# # フレーム数
# print(f"frame_count: {cap.get(cv2.CAP_PROP_FRAME_COUNT)}")
# # frame_count: 639.0

# # 再生時間
# print(f"length: {cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)} s")
# # length: 21.3 s

# print("fourcc: " + int(cap.get(cv2.CAP_PROP_FOURCC)).to_bytes(4, "little").decode("utf-8"))
# # fourcc: avc1
# # コーデックの種類を4文字で表すコード

