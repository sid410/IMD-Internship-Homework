import cv2
name = "Resources/lambo.PNG"
img = cv2.imread(name)
print(img.shape)
print(type(img))

#画像に文字を描画
cv2.putText(img,"This car is luxury.",(0,30),cv2.FONT_HERSHEY_DUPLEX,1,(255,255,255),cv2.LINE_4)
cv2.putText(img,"It's very costly but superb.",(180,420),cv2.FONT_HERSHEY_DUPLEX,1,(0,0,255),cv2.LINE_4)


if img is None:
    print("error")
else:

    cv2.imwrite(r'/Users/ys4-chan/Documents/GitHub/IMD-Internship-Homework/Tutorial/proof/lambo.jpg',img)
    cv2.imshow("lambo",img)

    cv2.waitKey(1)
    cv2.waitKey(0)

