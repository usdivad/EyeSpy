# EyeSpy!
# by David Su http://usdivad.com/
# 
# Usage: python eyespy.py
# 
# Adapted from https://github.com/shantnu/Webcam-Face-Detect by Shantnu Tiwari

import cv2
import OSC

import math
import sys 

if __name__ == '__main__':
    # OSC client setup
    client = OSC.OSCClient()
    client.connect(('127.0.0.1', 6448))

    # OpenCV setup
    cascPath = 'cascades/haarcascade_eye.xml' # default cascade
    if len(sys.argv) > 1:
        cascPath = sys.argv[1] # user-specified cascade
    cascade = cv2.CascadeClassifier(cascPath)

    # Webcam capture
    video_capture = cv2.VideoCapture(0)

    # Capture, analyze, and send OSC messages in a loop
    # until 'q' key is pressed
    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        detectedObjects = cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )

        # Draw a rectangle around the detectedObjects
        for (x, y, w, h) in detectedObjects:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow('Video', frame)

        # Extract features (eye-specific)
        eyes = detectedObjects
        eyes = sorted(eyes, key = lambda eye: eye[0])
        eyesCount = len(eyes)
        eyesAreas = [w*h for (x,y,w,h) in eyes]
        eyesAvgArea = 0
        leftEye_x, leftEye_y = (0, 0)
        rightEye_x, rightEye_y = (0, 0)
        leftRightEyeDistance = 0

        if eyesCount > 0:
            eyesAvgArea = reduce(lambda a1, a2: a1 + a2, eyesAreas) / len(eyes)
            leftEye_x, leftEye_y = (eyes[0][0], eyes[0][1])
            if eyesCount > 1:
                rightEye_x, rightEye_y = (eyes[1][0], eyes[1][1])

        leftRightEyeDistance = math.sqrt( ((leftEye_x + rightEye_x) ** 2) + ((leftEye_y + rightEye_y) ** 2))

        # Construct and send OSC message
        oscmsg = OSC.OSCMessage()
        oscmsg.setAddress('/wek/inputs')
        oscmsg.append(eyesCount)
        oscmsg.append(eyesAvgArea)
        oscmsg.append(leftRightEyeDistance)
        oscmsg.append(leftEye_x)
        oscmsg.append(leftEye_y)
        oscmsg.append(rightEye_x)
        oscmsg.append(rightEye_y)
        client.send(oscmsg)
        print oscmsg
        # print eyes

        # Break if 'q' key pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()