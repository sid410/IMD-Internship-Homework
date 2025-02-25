from ultralytics import YOLO
import cv2
import time

model_path = 'Project/yolov8s.pt' 

model = YOLO(model_path)  

video_path = "Project/Resources/automobile_video_hd.mp4"
cap = cv2.VideoCapture(video_path)


cv2.setNumThreads(0)

while cap.isOpened():
    start_time = time.time() 

    success, frame = cap.read()

    if success:

        results = model.predict(frame, conf=0.5, classes=[2, 7])  

        annotated_frame = results[0].plot()

        car_count = 0
        truck_count = 0

        for box in results[0].boxes:
            cls = int(box.cls.cpu().numpy()[0])
            label = results[0].names[cls]
            score = float(box.conf.cpu().numpy()[0])
            x1, y1, x2, y2 = box.xyxy.cpu().numpy()[0]

            if label == 'car':
                car_count += 1
            elif label == 'truck':
                truck_count += 1
      
        count_text = f"Cars: {car_count}  Trucks: {truck_count}"
       
        cv2.putText(annotated_frame, count_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow("YOLOv8 Inference", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()