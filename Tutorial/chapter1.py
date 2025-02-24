"""import cv2 #画像の出力
print("Package Imported")

img = cv2.imread("Resources/lena.png")

cv2.imshow("Output",img)
cv2.waitKey(0)
"""

"""import cv2 #動画の出力

cap = cv2.VideoCapture("Resources/test_video.mp4")

while True:
    success, img = cap.read()
    cv2.imshow("Video",img)
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break
"""

import cv2

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
cap.set(10,100)

while True:
    success, img = cap.read()
    cv2.imshow("Video",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
