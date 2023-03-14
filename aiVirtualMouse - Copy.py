import cv2
import numpy as np
import HandTrackingModule as hmt
import time
import autopy
#import volumecontrol
import sys


#########################
wCam, hCam = 640, 480
########################


cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
detector = hmt.HandDetector(maxhands=1)
#vc = volumecontrol.vcontroller
wScr, hScr = autopy.screen.size()
RframeR = 100
LframeR = 50
BframeR = 250
smoothening = 6
plocX, plocY = 0, 0
clocX, clocY = 0, 0
bool = True
autopy.mouse.Button.RIGHT
while True:

    #1. find hand landMarkes

    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    #2. gte the tip of the index and middle finger
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        x4, y4 = lmList[4][1:]
        #print(x1, y1, x2, y2)

        #3. check which fingers are up
        fingers = detector.fingersUp()
        #print(fingers)
        cv2.rectangle(img, (RframeR, 0), (wCam - LframeR, hCam - BframeR), (255, 0, 255), 3)


        #4. only index finger  : moving mode

        if fingers[1] == 1 and fingers[2] == 0 and fingers[0] == 0:

            # 5. convert coordinates
            x3 = np.interp(x1, (RframeR, wCam - LframeR), (0, wScr))
            y3 = np.interp(y1, (0, hCam - BframeR), (0, hScr))

            #6. smoothen values

            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            #7. move mouse


            autopy.mouse.move(wScr - clocX, clocY)
            cv2.circle(img, (x1,y1), 15,(255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY



        '''if fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 1:
            # 5. convert coordinates
            x3 = np.interp(x1, (RframeR, wCam - LframeR), (0, wScr))
            y3 = np.interp(y1, (0, hCam - BframeR), (0, hScr))

            # 6. smoothen values

            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            # 7. move mouse

            autopy.mouse.move(wScr - clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY
            length, img, lineInfo = detector.findDistance(8, 12, img, draw=False)
            print(length)
            if length < 40:

                if bool==True:

                    cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                    autopy.mouse.toggle(down=bool)
                    bool = False
                    time.sleep(0.3)

                else:

                    cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                    autopy.mouse.toggle(down=bool)
                    bool = True
                    time.sleep(0.3)

        #if fingers[4]==1 and fingers[1]==0:
            #time.sleep(1)
            #if fingers[2]==0 and fingers[3]==0:
                #vc.controlling(self=None)'''



        #8. both index and iddle fingers are up : clicking mode
        if fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 0:
            length, img, lineInfo = detector.findDistance(8, 12, img)
            #print(length)
            if length < 45:

                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()
                time.sleep(0.2)

        if fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 1:
            length, img, lineInfo = detector.findDistance(8, 12, img)
            #print(length)
            if length < 45:

                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click(autopy.mouse.Button.RIGHT)

                time.sleep(0.2)


            #if length > 50:
                #autopy.mouse.toggle(down=False)


    #9. find distance between fingers
    #10. click mouse if distance short
    #11. Frane rate

    cTime = time.time()
    print(cTime)
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN, 3,(255, 0, 0), 3)

    #12. display

    cv2.imshow("Image", img)
    cv2.waitKey(1)