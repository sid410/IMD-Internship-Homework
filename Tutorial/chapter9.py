import cv2


def size(i,j):
    if i<=0 or j<=0:
        print("もう一度入力して下さい")
        return 1
    else:
        return 0



def main():
    # 動画の読み取り
    cap = cv2.VideoCapture("Resources/test_video.mp4")

    while True:
        h = int(input("height:"))
        w = int(input("width:"))
        d = size(h,w)
        if d==1:
            print("もう一度入力して下さい。")
            continue
        elif d==0:
            break

    #動画の再生
    while True:#cap.isOpened():
        result, img = cap.read()
        #画像のサイズ変更
        img = cv2.resize(img,(h,w))
        cv2.imshow("Video", img)
        if cv2.waitKey(1) & 0xff == ord('d'):
            break

main()



