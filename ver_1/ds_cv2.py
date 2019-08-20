#import modules
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
#import RPi.GPIO as gpio

class opencv:
    def __init__(self):
        global cap, face_cascade, ret, frame
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        face_cascade = cv2.CascadeClassifier('/home/nuc/Documents/drivesense/ver_0/cascades/data/haarcascade_frontalface_alt2.xml')

    def openCam(init):
        while True:
            #ret, frame = cap.read()
            cv2.imshow('frame',frame)
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break
    
    def faceDetect(init):
        while True:
            #ret, frame = cap.read()
            cv2.imshow('frame',frame)
            faces = face_cascade.detectMultiScale(frame, scaleFactor=1.5, minNeighbors=5)
            for (x,y,w,h) in faces:
                roi_color = frame[y:y+h, x:x+w]
                #draws rectangle
                color = (255, 0, 0)
                stroke = 2
                end_cord_x = x+w
                end_cord_y = y+h
                cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)

            if cv2.waitKey(20) & 0xFF == ord('q'):
                break