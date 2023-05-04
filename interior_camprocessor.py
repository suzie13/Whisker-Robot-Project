import cv2
import time

cap = cv2.VideoCapture(2)
interval = 5 # interval in seconds
counter = 0 # initialize the counter

while True:
    ret, frame = cap.read()
    if ret:
        # Save the frame as an image with incrementing file name
        filename = f"image_{counter}.jpg"
        cv2.imwrite(filename, frame)
        counter += 1 # increment the counter variable
    time.sleep(interval)

cap.release()
