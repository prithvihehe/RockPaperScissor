import cv2
from cvzone.HandTrackingModule import HandDetector
import time
import random
import cvzone

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon = 0.8,  maxHands = 1)

count = 0
Start = False
initialTime = 0
Finish = False
scores = [0,0] 

cv2.namedWindow("Background", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Background", 1280, 720)



while True:
    #image
    success, img = cap.read()
    img = cv2.flip(img,1)
    imgScaled = cv2.resize(img,(0,0),None,0.625,0.775)
    
    #background
    background = cv2.imread(r"C:\Users\prith\OneDrive\Desktop\ML\RockPaperScissor\Images\ROCK PAPER AND SCISSOR.png")
    #webcam
    hands,imgScaled = detector.findHands(imgScaled, flipType = False)
    
    if Start:
        if Finish == False:
            count = time.time() - initialTime
            name = ['START','rock', 'paper', 'scissor'][int(count)]
            cv2.putText(background,name,(850,700),cv2.FONT_HERSHEY_PLAIN,5,(225,219,88),10)
            if count > 3:
                Finish = True
                count = 0
                if hands:
                    player = None
                    hand = hands[0]
                    finger = detector.fingersUp(hand)
                    
                    if finger == [1,0,0,0,0]:
                        player = 1 #rock
                    if finger == [0,1,1,1,1]:
                        player = 2 #paper
                    if finger == [1,1,1,0,0]:
                        player = 3 #scissor

                    computer = random.randint(1,3)
                    choice = cv2.imread(f'Images/{computer}.png', cv2.IMREAD_UNCHANGED)
                    background = cvzone.overlayPNG(background, choice, (400, 550))

                    # Player Wins
                    if (player == 1 and computer == 3) or(player == 2 and computer == 1) or (player == 3 and computer == 2):
                        scores[1] += 1

                    # Computer Wins
                    if (player == 3 and computer == 1) or(player == 1 and computer == 2) or (player == 2 and computer == 3):
                        scores[0] += 1

        if Finish:
            background = cvzone.overlayPNG(background,choice,(400, 550))
            cv2.putText(background,str(scores[0]),(700,380), cv2.FONT_HERSHEY_PLAIN,5,(255,0,0),7)     
            cv2.putText(background,str(scores[1]),(1700,380), cv2.FONT_HERSHEY_PLAIN,5,(0,255,0),7) 
            
    #display
    cv2.imshow("Background", background)
    cv2.imshow("Player", imgScaled)
    cv2.moveWindow("Player", 760,300)
    cv2.waitKey(1)
    if hands:
        newfinger = detector.fingersUp(hands[0])
        if newfinger == [0,0,1,1,1]:
            Start = True
            initialTime = time.time()
            Finish = False