import pyocr
import os
import cv2
import numpy as np
import sys
from PIL import Image,ImageEnhance

def detect(img):
    crop_size = img.shape[0] * img.shape[1]

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, img_th = cv2.threshold(img_gray, 190, 250, cv2.THRESH_OTSU)

    nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(img_th)

    if nlabels > 1:
        median = np.median(stats[:,4])
       
        for idx in range(1, nlabels):

            if( stats[idx][4] >= median * 2 ): # not average size
                img_th[labels == idx, ] = 0

            elif( stats[idx][4] < 5 ): # too small
                img_th[labels == idx, ] = 0

            elif( (stats[idx][4] / crop_size) > 0.25): # too big
                img_th[labels == idx, ] = 0

            else:
                pass
    img_th_im = Image.fromarray(img_th)
    text = tool.image_to_string(img_th_im , lang='eng', builder=builder)

    return img_th, text

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

file="Project/cut_en_sample.png"

# img = cv2.imread("Project/cut_en_sample.png")
# kernel = np.ones((5,5),np.uint8)

# ##gray
# imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# ##ぼかし
# imgBlur = cv2.GaussianBlur(imgGray,(1,1),0)
# ##輪郭
# imgCanny = cv2.Canny(imgBlur,200,200)
# ##輪郭膨張
# imgDialation = cv2.dilate(imgCanny,kernel,iterations=1)

# #ブラーなし
# imgCanny_no = cv2.Canny(img,200,200)
# ##輪郭膨張
# imgDialation_no = cv2.dilate(imgCanny_no,kernel,iterations=1)

# # OpenCVの画像（numpy.ndarray）をPIL.Imageに変換
# imgDialation_pil = Image.fromarray(imgDialation)

# enhancer= ImageEnhance.Contrast(imgDialation_pil) #コントラストを上げる
# img_con = enhancer.enhance(2.0) #コントラストを上げる

# # PIL.Image を numpy.ndarray に変換
# img_con_np = np.array(img_con)

# cv2.imshow("Dialation Image",imgDialation)
# cv2.imshow("Blur_no",imgDialation_no)
# cv2.imshow("Con",img_con_np)

img = cv2.imread(file)

img_result, text = detect(img)

print('Texto: ', text)
cv2.imshow('Resultado', img_result)
cv2.waitKey(0)
cv2.destroyAllWindows()

# txt_pyocr = tool.image_to_string(imgDialation_pil , lang='eng', builder=builder)

# print(txt_pyocr)

# cv2.waitKey(0)