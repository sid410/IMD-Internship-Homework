import cv2

input_video_path = 'Project/Resources/Human.mp4'  # 4K動画の入力ファイルパス
output_video_path = 'Project/Resources/Human_hd.mp4'  # 出力するHD動画のファイルパス

cap = cv2.VideoCapture(input_video_path)

fps = cap.get(cv2.CAP_PROP_FPS) 
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  

output_width = 1280
output_height = 720

out = cv2.VideoWriter(output_video_path, fourcc, fps, (output_width, output_height))

while cap.isOpened():
    success, frame = cap.read()

    if success:
        resized_frame = cv2.resize(frame, (output_width, output_height))

        out.write(resized_frame)

        cv2.imshow('Resized Video (HD)', resized_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
out.release()
cv2.destroyAllWindows()
