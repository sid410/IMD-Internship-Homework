#このプロジェクトはチュートリアルのStack関数をベースに参照して、暗視model、熱画像処理model、,色の簡略化model（cartoon model）(簡単版)を作成します。(モデル3ダイナミックキャプチャmodelは
# チャンスがあれば頑張ります)。


#まずは基本の先行コマンド
import cv2
import numpy as np


###########モデル（１）暗視model############
#まずはGama関数を設定する。
def adjust_gamma(image, gamma=1.5):
    invGamma = 1.0 / gamma
    ########0~255の間のピクセル値のガンマ調整####ガンマ調整関数は ((i/255.0) ** 1.5 * 255)の例に参照します。
    table = np.array([(i / 255.0) ** invGamma * 255 for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, table)


#緑の暗視効果
def night_vision_effect(image, gamma=3.5):
    corrected = adjust_gamma(image, gamma)
    green_channel = corrected.copy()
    green_channel[:, :, 0] = 0
    green_channel[:, :, 2] = 0

    return green_channel


#######モデル２熱画像処理model########
def thermal_vision_effect(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thermal = cv2.applyColorMap(gray, cv2.COLORMAP_JET)
    return thermal


##########モデル3ダイナミックキャプチャmodel（簡単な方法、トレニンーグに参照します。）######(この部分は未成功のコマンド)
#####失礼しました。この部分はまだ勉強の中に頑張ります。
#def motion_detection(frame, prev_frame):
# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#gray = cv2.GaussianBlur(gray, (5, 5), 0)
#if prev_gray is None:
#  return frame, gray
##フレーム差の計算
#frame_delta = cv2.absdiff(prev_frame, gray)
#_, thresh = cv2.threshold(frame_delta, 20, 255, cv2.THRESH_BINARY)
#thresh = cv2.dilate(thresh, None, iterations=2)
##輪郭を見つける
#contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
##色を作成する
#motion_frame = frame.copy()

#動的検出枠の描画
#for contour in contours:
#  if cv2.contourArea(contour) < 500:
#     continue
#    (x, y, w, h) = cv2.boundingRect(contour)
#   cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
#return motion_frame, gray

############モデル３色の簡略化model（cartoon model）(簡単版)#######
def cartoon_effect(image):
    #元の色の詳細を保持する
    color = cv2.edgePreservingFilter(image, flags=2, sigma_s=100, sigma_r=0.3)
    #エッジの抽出
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, 9, 12)
    #色の強調、アニメスタイルの模倣
    stylized = cv2.stylization(color, sigma_s=150, sigma_r=0.25)
    #最終的なアニメーション効果を合成する
    edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    cartoon = cv2.bitwise_and(stylized, edges)

    return cartoon


######Stack関数の参照#####
def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]),
                                                None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        hor_con = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver


    #カメラ
cap = cv2.VideoCapture(0)
#前のフレームを初期化します (動き検出用)
prev_gray = None
fps = int(cap.get(cv2.CAP_PROP_FPS))
if fps == 0:
    fps = 20
#エンコード形式の選択 (XVID、MJPG、MP4V)と複数の「VideoWriter」
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
fourcc = cv2.VideoWriter_fourcc(*"XVID")
#AVIファイルとして保存
out_night = cv2.VideoWriter("Night_Vision.avi", fourcc, fps, (frame_width, frame_height))
out_thermal = cv2.VideoWriter("Thermal_Vision.avi", fourcc, fps, (frame_width, frame_height))
out_cartoon = cv2.VideoWriter("Cartoon_Vision.avi", fourcc, fps, (frame_width, frame_height))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Applied of model
    gamma_corrected = adjust_gamma(frame, gamma=2.0)
    night_vision = night_vision_effect(gamma_corrected, gamma=3.5)
    thermal_vision = thermal_vision_effect(frame)
    #motion_detected, prev_gray = motion_detection(frame, prev_gray)
    cartoon_vision = cartoon_effect(frame)

    #この部分検定部分　実際操作(コマンドを動くする時)はこの部分の前に#付ける
    # cv2.imshow("original", frame)
    # cv2.imshow("night_vision", night_vision)
    # cv2.imshow("thermal_vision", thermal_vision)
    # #cv2.imshow("Motion Detection", motion_detected)
    # cv2.imshow("Cartoon Mode", cartoon_vision)

    #if cv2.waitKey(1) & 0xFF == ord('q'):
    #break

    #cap.release()
    #cv2.destroyAllWindows()

    Imagestack = stackImages(0.8, ([frame, night_vision],
                                   [thermal_vision, cartoon_vision]))
    cv2.imshow("The video of projiect", Imagestack)
    # ビデオファイルの書き込み
    out_night.write(night_vision)
    out_thermal.write(thermal_vision)
    out_cartoon.write(cartoon_vision)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
out_night.release()
out_thermal.release()
out_cartoon.release()
cap.release()
cv2.destroyAllWindows()
