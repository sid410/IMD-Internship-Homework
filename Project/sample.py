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
builder = pyocr.builders.TextBuilder(tesseract_layout=3)

file="Project/white.png"

img = cv2.imread(file)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


cv2.imshow("mask",gray)
cv2.waitKey(0)

mask_pil = Image.fromarray(gray)

txt_pyocr = tool.image_to_string(mask_pil , lang='eng', builder=builder)

print('Texto: ',txt_pyocr)
