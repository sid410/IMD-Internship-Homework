import pyocr
import os
import cv2
import numpy as np
import sys
from PIL import Image, ImageEnhance

tools = pyocr.get_available_tools()
tool = tools[0]
if len(tools) == 0:
    print("OCR tool is not found.")
    sys.exit(1)
lan = "eng"

# OCRエンジン取得
tools = pyocr.get_available_tools()
tool = tools[0]

# OCRの設定
builder = pyocr.builders.TextBuilder(tesseract_layout=6)

imgOri = cv2.imread('Project/Resources/cut_en_sample.png')

kernel = np.array([[ 0, -0.5,  0],
                   [-0.5,  3, -0.5],
                   [ 0, -0.5,  0]])

imgHSV = cv2.cvtColor(imgOri, cv2.COLOR_BGR2HSV)
imgBlur = cv2.GaussianBlur(imgHSV, (9,9), 0)
imgSharp = cv2.filter2D(imgBlur, -1, kernel)

lower = np.array([0, 0, 190])
upper = np.array([255, 255, 255])
imggray = cv2.inRange(imgSharp, lower, upper)
# cv2.imshow("Gray", imggray)

imgGray=cv2.cvtColor(imggray,cv2.COLOR_GRAY2RGB)


ret, dst = cv2.threshold(imggray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

img = cv2.cvtColor(dst, cv2.COLOR_GRAY2RGB)

contours, hierarchy = cv2.findContours(dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

contours_subset = []

for c in contours:
    area = cv2.contourArea(c)
    if area > 5000:
        contours_subset.append(c)

mask = np.zeros_like(imggray, dtype=np.uint8)

cv2.drawContours(mask, contours_subset, -1, (255), thickness=cv2.FILLED)

# cv2.imshow("mask", mask)

# 背景を白にする
background_white = np.full_like(imgOri, 255, dtype=np.uint8)  # 真っ白の背景画像を作成

# マスクの白部分は元画像を使い、それ以外を白にする
result = np.where(mask[:, :, None] == 255, imgGray, background_white)

# cv2.imshow("result", result)

# cv2.waitKey(0)
# cv2.destroyAllWindows()

mask_pil = Image.fromarray(result)

txt_pyocr = tool.image_to_string(mask_pil , lang='eng', builder=builder)

print('Texto: ',txt_pyocr)