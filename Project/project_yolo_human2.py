from ultralytics import YOLO
import cv2
import time
import numpy as np
from collections import defaultdict

model_path = 'Project/yolov8s.pt' 
model = YOLO(model_path)  

video_path = "Project/Resources/Human_hd.mp4"
cap = cv2.VideoCapture(video_path)

cv2.setNumThreads(0)

group_threshold = 43 

def get_centroid(box):
    x1, y1, x2, y2 = box
    return (x1 + x2) / 2, (y1 + y2) / 2

while cap.isOpened():
    start_time = time.time()
    success, frame = cap.read()

    if success:
        results = model.predict(frame, conf=0.2, classes=[0])  
        annotated_frame = results[0].plot()

        person_boxes = []
        centroids = []

        for box in results[0].boxes:
            cls = int(box.cls.cpu().numpy()[0])
            label = results[0].names[cls]
            if label == 'person':
                x1, y1, x2, y2 = box.xyxy.cpu().numpy()[0]
                person_boxes.append([x1, y1, x2, y2])
                centroids.append(get_centroid([x1, y1, x2, y2]))

        groups = defaultdict(list)
        used = set()

        for i, centroid1 in enumerate(centroids):
            if i in used:
                continue
            group = [person_boxes[i]]
            used.add(i)

            for j, centroid2 in enumerate(centroids):
                if j in used:
                    continue
                dist = np.linalg.norm(np.array(centroid1) - np.array(centroid2))
                if dist < group_threshold:
                    group.append(person_boxes[j])
                    used.add(j)

            if len(group) >= 2:
                groups[len(groups)] = group

        for group in groups.values():
            x1_min = min(box[0] for box in group)
            y1_min = min(box[1] for box in group)
            x2_max = max(box[2] for box in group)
            y2_max = max(box[3] for box in group)
            
            cv2.rectangle(annotated_frame, (int(x1_min), int(y1_min)), (int(x2_max), int(y2_max)), (0, 255, 0), 3)
            cv2.putText(annotated_frame, f"Group ({len(group)})", (int(x1_min), int(y1_min) - 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)

        count_text = f"Person: {len(person_boxes)} Groups: {len(groups)}"
        cv2.putText(annotated_frame, count_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.imshow("YOLOv8 Inference", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
