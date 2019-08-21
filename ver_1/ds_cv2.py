from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
from threading import Thread
import numpy as np
#from playsound import playsound
import argparse
import imutils
import time
import dlib
import cv2
import os
import RPi.GPIO as gpio 

class opencv:
    def __init__(self):
        global cap, ret, frame, face_cascade, ear, THRESH, CONSEC_FRAMES, detector, predictor, lStart, lEnd, rStart, rEnd, vs, fileStream, ap, TOTAL, COUNTER 
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        THRESH = 0.3
        CONSEC_FRAMES = 40  
        
        COUNTER = 0
        TOTAL = 0
        
        gpio.setmode(gpio.BCM)

        gpio.setup(25, gpio.OUT)
        ap = argparse.ArgumentParser()
        ap.add_argument("-p", "--shape-predictor", required=True,
	    help="path to facial landmark predictor")
        ap.add_argument("-v", "--video", type=str, default="",
	    help="path to input video file")
        args = vars(ap.parse_args())
        #face_cascade = cv2.CascadeClassifier('/home/nuc/Documents/drivesense/ver_0/cascades/data/haarcascade_frontalface_alt2.xml')

    def openCam(init):
        while True:
            cv2.imshow('frame', frame)
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

    def eye_aR(init, eye):
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])
    
        # compute the euclidean distance between the horizontal
        # eye landmark (x, y)-coordinates
        C = dist.euclidean(eye[0], eye[3])
    
        # compute the eye aspect ratio
        ear = (A + B) / (2.0 * C)
    
        # return the eye aspect ratio
        return ear
    
    def drowsinessDetect(init, ):
        print("[INFO] loading facial landmark predictor...")
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(args["shape_predictor"])

        (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"] #index for left eye
        (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

        print("[INFO] starting video stream thread...")
        vs = FileVideoStream(args["video"]).start()
        #fileStream = True
        #vs = VideoStream(src=0).start()
        vs = VideoStream(usePiCamera=True).start()
        fileStream = False
        time.sleep(1.0)

        while True:
	        if fileStream and not vs.more():
		        break
            frame = vs.read()
            frame = imutils.resize(frame, width=450)
	        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            rects = detector(gray, 0) 

            for rect in rects:
                shape = predictor(gray, rect)
                shape = face_utils.shape_to_np(shape) #converts to np array

                leftEye = shape[lStart:lEnd]
                rightEye = shape[rStart:rEnd]
                leftEAR = eye_aR(leftEye)
                rightEye = eye_aR(rightEye)

                # getting convex hull
                leftEyeHull = cv2.convexHull(leftEye)
                rightEyeHull = cv2.convexHull(rightEye)
                # drawing contours
                cv2.drawContours(frame, [leftEyeHull], -1, (0, 0, 255))
                cv2.drawContours(frame, [rightEyeHull], -1, (0, 0, 255))

                if ear < THRESH:
                    COUNTER += 1
                    if COUNTER >= CONSEC_FRAMES:
                        TOTAL += 1
                        gpio.output(25, 1)
                        time.sleep(0.0025)
                        gpio.output(25, 0)
                        time.sleep(0.0025)
                        cv2.putText(frame, "DROWSINESS DETECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                else:
                    COUNTER = 0
                    gpio.output(25, 0)

                cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            cv2.imshow("frame", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q')
                break
        
        cv2.destroyAllWindows()
        vs.stop()