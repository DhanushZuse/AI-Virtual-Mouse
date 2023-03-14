import cv2
import time
import numpy as np
import HandTrackingModule as htm
import sys

import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
class vcontroller:
    def controlling(self):
        ####################################
        wCam, hCam = 640, 480
        ####################################

        cap = cv2.VideoCapture(0)
        cap.set(3, wCam)
        cap.set(4, hCam)
        pTime = 0
        cTime = 0
        vol = 0
        volBar = 400
        volPer = 0
        colorVol = (255, 0, 0)
        detector = htm.HandDetector(detectioncon=0.7,maxhands=1)

        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        #volume.GetMute()
        #volume.GetMasterVolumeLevel()
        volRange = volume.GetVolumeRange()
        minVol = volRange[0]
        maxVol = volRange[1]
        area = 0
        a = 0
        while True:
            success, img = cap.read()

            # Find Hand
            img = detector.findHands(img)
            lmList, bbox = detector.findPosition(img, draw=True)

            if len(lmList) != 0:

                # Filter  based on size
                area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1]) // 100
                # print(area)
                if 450 < area < 1100:
                    # print("yes")
                    # find distance between index and thumb
                    length, img, lineInfo = detector.findDistance(4, 8, img)
                    # print(length)

                    # convert volume
                    vol = np.interp(length, [35, 250], [minVol, maxVol])
                    volBar = np.interp(length, [35, 250], [400, 150])
                    volPer = np.interp(length, [35, 250], [0, 100])

                    # reduce resolution to make it smoother
                    smoothness = 10
                    volPer = smoothness * round(volPer / smoothness)

                    # check fingers up
                    fingers = detector.fingersUp()
                    # print(fingers)

                    # if pinky is down set volume
                    if not fingers[3]:
                        volume.SetMasterVolumeLevelScalar(volPer / 100, None)
                        cv2.circle(img, (lineInfo[4], lineInfo[5]), 10, (0, 255, 0), cv2.FILLED)
                        colorVol = (0, 255, 0)
                    else:
                        colorVol = (255, 0, 0)

                    #if not fingers[4]:
                        #sys.exit()

                    # print(lmList[4], lmList[8])

                    #x1, y1 = lmList[4][1], lmList[4][2]
                    #x2, y2 = lmList[8][1], lmList[8][2]
                    #cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

                    #cv2.circle(img, (x1, y1), 10, (255, 0, 0), cv2.FILLED)
                    #cv2.circle(img, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
                    #cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)
                    #cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

                    #length = math.hypo(x2 - x1, y2 - y1)
                    # print(length)
                    # handRange 50 - 300
                    # volume range = -65 - 0
            # drawing

            cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
            cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, f'{int(volPer)}% ', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
            cVol = int(volume.GetMasterVolumeLevelScalar() * 100)
            cv2.putText(img, f'Vol Set: {int(cVol)}% ', (400, 50), cv2.FONT_HERSHEY_COMPLEX, 1, colorVol, 2)

            # frame rate

            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            cv2.putText(img,f'FPS:{int(fps)}', (17, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

            cv2.imshow("img", img)
            

