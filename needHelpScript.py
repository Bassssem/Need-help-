import cv2
import mediapipe as mp
import threading
import winsound

def HelpSound():
    winsound.PlaySound("help.wav", winsound.SND_FILENAME)

def DrinkSound():
    winsound.PlaySound("drink.wav", winsound.SND_FILENAME)

def cam():
    cap = cv2.VideoCapture(0)
    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils
    fingerCoordinates = [(8, 6), (12, 10), (16, 14), (20, 18)]
    thumbCoordinate = (4,2)
    rep=[]
    cord=[0,0]
    while True:
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        multiLandMarks = results.multi_hand_landmarks

        if multiLandMarks:
            handPoints = []
            for handLms in multiLandMarks:
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

                for idx, lm in enumerate(handLms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    handPoints.append((cx, cy))

            for point in handPoints:
                cv2.circle(img, point, 10, (0, 0, 255), cv2.FILLED)

            upCount = 0
            
            for coordinate in fingerCoordinates:
                if handPoints[coordinate[0]][1] < handPoints[coordinate[1]][1]:
                    upCount += 1
            if handPoints[thumbCoordinate[0]][0] > handPoints[thumbCoordinate[1]][0]:
                upCount += 1
            if upCount!=0:
                cv2.putText(img,"00:00:"+str(15-len(rep))+"S", (460,30), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 3)

            if len(rep)==0:
                rep.append(upCount)
            else:
                if upCount==rep[-1]:
                    rep.append(upCount)
                    if len(rep)==15:
                        if rep[0]==5:
                            DrinkSound()
                            rep=[]
                        elif rep[0]==0:
                            HelpSound()
                            rep=[]
                else:
                    rep=[]

        cv2.imshow("need help !", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release() 
    cv2.destroyAllWindows()

opencv = threading.Thread(target=cam)
opencv.start()
