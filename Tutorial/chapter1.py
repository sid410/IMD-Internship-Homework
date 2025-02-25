import cv2


img = cv2.imread("Resources/1.jpg")

#画像をグレー化する
grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#灰色化した画像を表示
cv2.imshow("Gray Image",grayscale)

cv2.waitKey(0)
