import cv2
path = "Resources/shapes.png"
img = cv2.imread(path)
#print(type(path))
#print(type(img))




if path is None:
    print("error")
else:
    print(img.shape)
    #高さと幅を自分で設定して画像を出力
    while True:
        h = int(input("高さを設定して下さい:"))
        w = int(input("幅をせってして下さい:"))
        if h<=0 or w<=0:#hまたはwが負の数であれば再入力
            print("エラー発生。もう一度入力して下さい。")
            continue
        else:
            break
    size = cv2.resize(img,(w,h))
    cv2.imwrite(r'/Users/ys4-chan/Documents/GitHub/IMD-Internship-Homework/Tutorial/proof/shapes1.jpg',img)
    cv2.imshow("img",size)
    cv2.waitKey(0)



