import cv2
import numpy as np 

#cap = cv2.VideoCapture("eye-recording.flv")
cap = cv2.VideoCapture("eye-tracking.mp4")
while True:
    ret, frame = cap.read()
    roi = frame[114: 500, 0: 500] #y, x
    #roi = frame[207: 585, 400: 958]
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
    _, threshold = cv2.threshold(gray_roi, 5, 255, cv2.THRESH_BINARY)

    cv2.imshow('treshold',threshold)
    cv2.imshow('gray_roi', gray_roi)
    cv2.imshow('frame', roi)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()