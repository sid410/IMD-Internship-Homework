import cv2
import random

r = random.randint(1,9)
#print("COMが好きに決めて下さい。")
print(r)

#AI(COM)に本の画像をどうし変更するのを勝手に決めさせる。
if r == 1 and 2 and 3:
    img = cv2.imread("Resources/book.jpg")
    color = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.imshow("color", color)
    cv2.waitKey(0)
elif r == 4 and 5 and 6:
    img = cv2.imread("Resources/book.jpg")
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    cv2.imshow("Gray",img)
    cv2.waitKey(0)
else:
    name = "Resources/book.jpg"
    img = cv2.imread(name)
    # 画像に文字を描画
    cv2.putText(img, "This book is so difficult.", (0, 30), cv2.FONT_HERSHEY_TRIPLEX, 1, (100, 300, 100), cv2.LINE_4)
    #cv2.putText(img, "It's very costly but superb.", (180, 420), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), cv2.LINE_4)

    cv2.imshow("book", img)
    cv2.waitKey(1)
    cv2.waitKey(0)

