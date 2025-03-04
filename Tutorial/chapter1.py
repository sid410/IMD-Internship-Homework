#image
import os
print("Current Directory:", os.getcwd())

import cv2
print("Package Imported")

##img = cv2.imread("Resources/lena.png")
img = cv2.imread("/Users/ryosuke371/Documents/GitHub/IMD-Internship-Homework/Tutorial/Resources/lena.png")

cv2.imshow("Output",img)
cv2.waitKey(0)

#video
# import cv2

# cap = cv2.VideoCapture("/Users/ryosuke371/Documents/GitHub/IMD-Internship-Homework/Tutorial/Resources/test_video.mp4")

# while True:
#     success, img = cap.read()
#     cv2.imshow("Video",img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# 

#camera
# import cv2

# cap = cv2.VideoCapture(0)
# cap.set(3,600)
# cap.set(4,480)
# cap.set(10,100)

# while True:
#     success, img = cap.read()
#     cv2.imshow("Video",img)
#     if cv2.waitKey(1) & 0xFF ==ord('q'):
#         break