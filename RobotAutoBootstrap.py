import os
import time
import cv2
from pyzbar.pyzbar import decode

import Robot.AutoCameraStreamer as ACS

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    detectedCodes = decode(frame)
    for code in detectedCodes:
        print(code.data)
        (x, y, w, h) = code.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 5)
    ACS.switch(frame)
    time.sleep(0.02)
    #cv2.imshow('QR', frame)
    #cv2.waitKey(20)


