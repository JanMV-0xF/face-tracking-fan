import numpy as np
import serial
import time
import sys
import cv2

# Setup Communication path for Arduino (In place of 'COM5' put the port to which your Arduino is connected)
arduino = serial.Serial('com4', 9600)
time.sleep(2)
print("Connected to Arduino...")

# Importing the Haarcascade for face detection
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# To capture the video stream from the webcam
cap = cv2.VideoCapture(0)

# Check if the video capture is opened successfully
if not cap.isOpened():
    print("Error: Could not open video stream.")
    sys.exit()

# Read the captured image, convert it to Gray image and find faces
while True:
    ret, img = cap.read()

    if not ret:
        print("Error: Could not read frame from video stream.")
        break

    # Flip the image horizontally
    img = cv2.flip(img, 1)

    # Draw guide lines
    cv2.line(img, (500, 250), (0, 250), (0, 255, 0), 1)
    cv2.line(img, (250, 0), (250, 500), (0, 255, 0), 1)
    cv2.circle(img, (250, 250), 5, (255, 255, 255), -1)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply histogram equalization to improve contrast
    gray = cv2.equalizeHist(gray)

    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,  # Adjusted for better accuracy
        minNeighbors=5,   # Adjusted for better accuracy
        minSize=(30, 30), # Minimum size of the face to detect
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Detect the face and make a rectangle around it
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 5)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]

        # Center of roi (Rectangle)
        xx = x + w // 2
        yy = y + h // 2

        center = (xx, yy)

        # Sending data to Arduino
        data = 'X{0:d}Y{1:d}Z'.format(int(xx), int(yy))
        arduino.write(data.encode())

    # Display the stream
    cv2.imshow('img', img)

    # Hit 'q' to terminate execution
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
