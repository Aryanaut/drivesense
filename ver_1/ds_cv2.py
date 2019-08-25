"""

    ds_cv2.py 
    Author: Aryan Mahesh
    Description: Main code of DriveSense that detects the drowsiness of the user and beeps if detected
    Sources: https://www.pyimagesearch.com/2017/04/24/eye-blink-detection-opencv-python-dlib/
             https://www.pyimagesearch.com/2018/07/19/opencv-tutorial-a-guide-to-learn-opencv/

"""

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
from ds_sms import sms
from ds_gps import GPS
from ds_accel import ADXL

class cv:
    global a
    a = ADXL()
    def __init__(self):
        global sms, g, a, fileStream, gray, vs, ap, detector, predictor, lStart, lEnd, rStart, rEnd
        gpio.setmode(gpio.BCM)
        gpio.setup(25, gpio.OUT) # setting the speaker up
        gpio.setup(21, gpio.IN) # panic button
        gpio.output(25, 1)
        sms = sms()
        g = GPS()


    def eye_aR(self, eye):
        # compute the euclidean distances between the two sets of
        # vertical eye landmarks (x, y)-coordinates
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])

        # compute the euclidean distance between the horizontal
        # eye landmark (x, y)-coordinates
        C = dist.euclidean(eye[0], eye[3])

        # compute the eye aspect ratio
        ear = (A + B) / (2.0 * C)

        # return the eye aspect ratio
        return ear

    def drowsinessDetect(self):
        ap = argparse.ArgumentParser()
        ap.add_argument("-p", "--shape-predictor", required=True,
            help="path to facial landmark predictor")
        ap.add_argument("-v", "--video", type=str, default="",
            help="path to input video file")
        args = vars(ap.parse_args())

        print("[INFO] loading facial landmark predictor...")
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(args["shape_predictor"])
        (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
        
        COUNTER = 0
        TOTAL = 0
        
        THRESH = 0.3
        CONSEC_FRAMES = 30
        vs = FileVideoStream(args["video"]).start()
        print("[INFO] loading video stream thread...")
        #fileStream = True
        #vs =VideoStream(src=0).start()
        vs = VideoStream(usePiCamera=True).start()
        fileStream = False
        time.sleep(1.0)

        while True:
            if fileStream and not vs.more:
                break
            frame = vs.read()
            frame = imutils.resize(frame, width=850)
            gray =  cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # grayscale
            rects = detector(gray, 0)

            for rect in rects:
                shape = predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)

                leftEye = shape[lStart:lEnd]
                rightEye = shape[rStart:rEnd]

                leftEAR = self.eye_aR(leftEye)
                rightEAR = self.eye_aR(rightEye)
                # average EAR
                ear = (leftEAR + rightEAR) / 2.0

                # convex hull
                leftEyeHull = cv2.convexHull(leftEye)
                rightEyeHull = cv2.convexHull(rightEye)

                # drawing contours
                cv2.drawContours(frame, [leftEyeHull], -1, (0, 0, 255), 1)
                cv2.drawContours(frame, [rightEyeHull], -1, (0, 0, 255), 1)

                if ear < THRESH:
                    COUNTER += 1
                    if COUNTER >= CONSEC_FRAMES:
                        TOTAL += 1
                        if COUNTER >= CONSEC_FRAMES:
                            TOTAL += 1

                            gpio.output(25, 0)
                            #time.sleep(0.0025)
                            #gpio.output(25, 0)
                            #time.sleep(0.0025)
                            cv2.putText(frame, "DROWSINESS DETECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                else:
                    COUNTER = 0
                    gpio.output(25, 1)
                    time.sleep(0.5)

                cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            cv2.imshow('frame', frame)
            key = cv2.waitKey(1) & 0xFF
            g.readAndDecode()
            lnk = g.link()
            m = "Crash at "+lnk
            if a.check_evt():
                sms.sendMSG('+919740254990', m)
                sms.sendWhatsapp('whatsapp:+919036430733', m)
                print("OK")

            if gpio.input(21) == 1:
                print("DETECTED")
                sms.sendMSG("+919740254990", "Panic alert at"+m)
                print("OK")

            if key == ord('q'):
                break
            

        cv2.destroyAllWindows()
        gpio.cleanup()
        vs.stop()