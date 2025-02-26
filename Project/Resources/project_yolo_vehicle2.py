from ultralytics import YOLO
import cv2
import time
import numpy as np

# モデルのロード
model_path = 'Project/yolov8n-seg.pt'
model = YOLO(model_path)  

video_path = "Project/Resources/automobile_video_hd.mp4"
cap = cv2.VideoCapture(video_path)

cv2.setNumThreads(0)

def get_dominant_color(image, mask):
    """
    マスクされた領域の代表的な色を取得
    """
    mask_resized = cv2.resize(mask, (image.shape[1], image.shape[0]))  # マスクをフレームサイズにリサイズ
    masked_pixels = image[mask_resized > 0]  # マスクされたピクセルのみ取得

    if len(masked_pixels) == 0:
        return (128, 128, 128)  # デフォルトのグレー

    # K-means クラスタリングで代表的な色を求める
    masked_pixels = np.float32(masked_pixels)
    k = 2  # クラスタ数（主要な色を2種類抽出）
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, labels, centers = cv2.kmeans(masked_pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # 最も多く出現する色を選択
    dominant_color = centers[np.argmax(np.bincount(labels.flatten()))]
    return tuple(map(int, dominant_color))  # (B, G, R) 形式で返す

while cap.isOpened():
    start_time = time.time()
    success, frame = cap.read()

    if success:
        results = model.predict(frame, conf=0.5, classes=[2, 7])  # car(2) & truck(7)
        annotated_frame = results[0].plot()

        car_count = 0
        truck_count = 0

        if results[0].masks is not None:  # セグメンテーションマスクがあるか確認
            for i, box in enumerate(results[0].boxes):
                cls = int(box.cls.cpu().numpy()[0])
                label = results[0].names[cls]
                x1, y1, x2, y2 = map(int, box.xyxy.cpu().numpy()[0])

                mask = results[0].masks.data[i].cpu().numpy()  # マスクを取得
                mask = (mask * 255).astype(np.uint8)  # 0-255に変換

                # マスクのサイズをフレームに合わせる
                dominant_color = get_dominant_color(frame, mask)

                # クラスに応じてカウント
                if label == 'car':
                    car_count += 1
                elif label == 'truck':
                    truck_count += 1

                # ボックス描画
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), dominant_color, 2)
                cv2.putText(annotated_frame, f"{label} - {dominant_color}", (x1, y1 - 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, dominant_color, 2, cv2.LINE_AA)

        count_text = f"Cars: {car_count}  Trucks: {truck_count}"
        cv2.putText(annotated_frame, count_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.imshow("YOLOv8 Inference", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
