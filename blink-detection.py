#import modules
from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
from threading import Thread
import numpy as np
from playsound import playsound
import argparse
import imutils
import time
import dlib
import cv2

def sound_alarm(path):
	# play an alarm sound
	playsound.playsound(path)

def eye_aR(eye):
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

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True,
	help="path to facial landmark predictor")
ap.add_argument("-v", "--video", type=str, default="",
	help="path to input video file")
args = vars(ap.parse_args())

EYE_THRESH = 0.3 #threshold for the eye. if it closes further then it is a blink
EYE_CONSEC_FRAMES = 3 #number of frames the eye should be closed for it to be a blink

COUNTER = 0
TOTAL = 0

print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"] #index for left eye
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

print("[INFO] starting video stream thread...")
vs = FileVideoStream(args["video"]).start()
#fileStream = True
vs = VideoStream(src=0).start()
# vs = VideoStream(usePiCamera=True).start()
fileStream = False
time.sleep(1.0)

while True:
	if fileStream and not vs.more():
		break

	frame = vs.read()
	frame = imutils.resize(frame, width=450)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #grayscale

	rects = detector(gray, 0) #detects the faces

	for rect in rects:
		shape = predictor(gray, rect)
		shape = face_utils.shape_to_np(shape) #converts facial landmarks into np array

		leftEye = shape[lStart:lEnd] 
		rightEye = shape[rStart: rEnd]
		leftEAR = eye_aR(leftEye)
		rightEAR = eye_aR(rightEye)
		#average EAR of both eyes
		ear = (leftEAR + rightEAR) / 2.0

		# get convex hull of the eye
		leftEyeHull = cv2.convexHull(leftEye)
		rightEyeHull = cv2.convexHull(rightEye)

		#draw contours around the area of the eye
		cv2.drawContours(frame, [leftEyeHull], -1, (0, 0, 255), 1)
		cv2.drawContours(frame, [rightEyeHull], -1, (0, 0, 255), 1)

		#adds to the counter 
		if ear < EYE_THRESH:
			COUNTER += 1

		else:
			if COUNTER >= EYE_CONSEC_FRAMES:
				TOTAL += 1
				playsound("beep-02.wav")

			# reset the counter
			COUNTER = 0

		cv2.putText(frame, "Blinks: {}".format(TOTAL), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

		cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

	cv2.imshow('frame', frame)
	key = cv2.waitKey(1) & 0xFF

	if key == ord('q'):
		break

cv2.destroyAllWindows()
vs.stop()





