import cv2
print("hello")
img = cv2.imread("Resources/book.jpg")

color = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

cv2.imshow("Image",img)
cv2.imshow("color",color)

cv2.waitKey(0)
