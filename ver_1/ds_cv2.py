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

class opencv:
    def __init__(self):
        global cap, ret, frame, face_cascade
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        #face_cascade = cv2.CascadeClassifier('/home/nuc/Documents/drivesense/ver_0/cascades/data/haarcascade_frontalface_alt2.xml')

    def openCam(init):
        while True:
            cv2.imshow('frame', frame)
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
    
    