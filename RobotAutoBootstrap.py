import os
import time
import cv2
from pyzbar.pyzbar import decode

import Robot.AutoCameraStreamer as ACS

cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

font = cv2.FONT_HERSHEY_SIMPLEX
blc_x = 10
blc_y = 40
fontScale = 0.7
fontColor = (255, 0, 0)
thickness = 2
lineType = 2

step = 40

while True:
    ret, frame = cap.read()
    detectedCodes = decode(frame)
    ctr = 0
    for code in detectedCodes:
        cv2.putText(frame, str(code.data)[2:],
                    (blc_x, blc_y+step*ctr),
                    font,
                    fontScale,
                    fontColor,
                    thickness,
                    lineType)
        (x, y, w, h) = code.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 5)
        ctr+=1
    ACS.switch(cv2.imencode('.jpg', frame)[1].tobytes())
    time.sleep(0.02)
    # cv2.imshow('QR', frame)
    # cv2.waitKey(20)
