import pyocr
import os
import cv2
import numpy as np
import sys
from PIL import Image,ImageEnhance

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

path="Project/cut_en_sample_2.png"
# path="Project/sample.png"

kernel = np.array([[ 0, -0.5,  0],
                   [-0.5,  3, -0.5],
                   [ 0, -0.5,  0]])

img = cv2.imread(path)
imgHSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
imgBlur = cv2.GaussianBlur(imgHSV,(9,9),0)
imgSharp = cv2.filter2D(imgBlur,-1,kernel)
lower=np.array([0,0,190])
upper=np.array([255,255,255])
mask=cv2.inRange(imgSharp,lower,upper)

cv2.imshow("mask",mask)
cv2.waitKey(0)

mask_pil = Image.fromarray(mask)

txt_pyocr = tool.image_to_string(mask_pil , lang='eng', builder=builder)

print(txt_pyocr)