import cv2 as cv
import mediapipe as mp
import time

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

cap = cv.VideoCapture(0)

while True:
    _, frame = cap.read()
    frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                # print(id,lm)
                h, w, c = frame.shape
                cx,cy = int(lm.x*w),int(lm.y*h)
                print(id, cx,cy) 
                if id ==0:  # find location of individual landmark
                    cv.circle(frame,(cx,cy), 25,(0,255,0),cv.FILLED)

            mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)




    cv.imshow("o9maga",frame)
    cv.waitKey(1)