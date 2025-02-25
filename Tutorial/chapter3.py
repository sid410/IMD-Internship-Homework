import cv2


#image_path = "IMD-internship-Homework/Tutorial/Resources/book.jpg"
#print(os.getcwd())

#if image_path is not os.path.exists(image_path):
    #print("error1")

path = r"Resources/book.jpg"
img = cv2.imread(path)

if img is None:
    print("error")
#画像のサイズを取得
#h,w = img.shape[:2]

#画像のサイズを2倍にする
else:
    print("OK")
    result = cv2.resize(img,(300,200))#画像のサイズを幅300,高さ200にした。
    #resultが存在していなければ"error"を出す。
    if result is None:
        print("error")

    else:
        print("OK")
        cv2.imshow("Image",result)
        cv2.waitKey(5)
        cv2.waitKey(0)
        #cv2.destroyAllwindows()


