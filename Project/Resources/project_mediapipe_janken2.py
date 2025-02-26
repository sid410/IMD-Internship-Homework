import cv2
import mediapipe as mp
import random
import time

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

gestures = ["rock", "scissors", "paper"]  

def recognize_gesture(hand_landmarks): #じゃんけんの手を判定
    tips = [4, 8, 12, 16, 20] 
    mcps = [2, 5, 9, 13, 17] 

    open_fingers = 0  

    for tip, mcp in zip(tips[1:], mcps[1:]):  # 親指以外の開いている数
            if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[mcp].y:
                open_fingers += 1  
        
    is_thumb_open = hand_landmarks.landmark[4].x > hand_landmarks.landmark[2].x  # 親指の判定

    #自分の手を決める
    if open_fingers == 0 and is_thumb_open == False:
        return "rock"
    elif open_fingers == 2 and is_thumb_open == False:
        return "scissors"
    elif open_fingers == 4 and is_thumb_open == True:
        return "paper"
    else:
        return "None"

def determine_winner(player, npc): #勝敗の判定
    if player == npc:
        return "Draw"
    elif ((player == "rock" and npc == "scissors") or 
         (player == "scissors" and npc == "paper") or 
         (player == "paper" and npc == "rock")):
        return "You Win!"
    else:
        return "You Lose!"

cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
    
    game_active = False  
    countdown_start_time = None  
    npc_gesture = None  
    result = ""  
    saved_player_gesture = "None"

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # 画像をRGBに変換
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        # 画像をBGRに戻す
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        player_gesture = saved_player_gesture if npc_gesture is not None else "None"

        if results.multi_hand_landmarks and npc_gesture is None:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

                # じゃんけんの手の形を判定
                player_gesture = recognize_gesture(hand_landmarks)
                saved_player_gesture = player_gesture  # 結果が決まる前に手の形を保存

        # 画像を左右反転（カメラ映像を見やすくするため）
        image = cv2.flip(image, 1)

        # ゲームが始まっていない場合、Enterキーで開始
        if not game_active and cv2.waitKey(1) & 0xFF == 13:  # Enterキー
            game_active = True
            countdown_start_time = time.time()
            npc_gesture = None
            result = ""

        # ゲームが開始されたらカウントダウン
        if game_active:
            elapsed_time = time.time() - countdown_start_time
            if npc_gesture is None:  # NPCがまだ手を出していない場合
                if elapsed_time < 3:  # 3秒カウントダウン
                    countdown_number = 3 - int(elapsed_time)
                    cv2.putText(image, str(countdown_number), (250, 250), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 255), 5, cv2.LINE_AA)
                else:  # 3秒経過後にNPCの手を決定
                    npc_gesture = random.choice(gestures)
                    result = determine_winner(saved_player_gesture, npc_gesture)

        # プレイヤーの手を表示
        cv2.putText(image, f"Player: {saved_player_gesture}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # NPCの手が決まっていたら表示
        if npc_gesture is not None:
            cv2.putText(image, f"NPC: {npc_gesture}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(image, result, (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(image, "Press Enter to play again", (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

        cv2.imshow('janken', image)

        # 結果が表示された後にEnterキーを押すまで待つ
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESCキーで終了
            break
        elif key == 13 and npc_gesture is not None:  # Enterキーで再試合
            game_active = False
            countdown_start_time = None
            npc_gesture = None
            result = ""

cap.release()
cv2.destroyAllWindows()
