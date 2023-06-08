import cv2
import time
import os
from datetime import datetime

cap = cv2.VideoCapture(14)
interval = 0.04  # interval in seconds (25 frames per second)(25Hz)
counter = 0  # initialize the counter

output_folder = "output"

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

while True:
    ret, frame = cap.read()
    if ret:
        # Get the current date and time as a string
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save the frame as an image with the timestamp as the filename
        filename = os.path.join(output_folder, f"image_{timestamp}.jpg")
        cv2.imwrite(filename, frame)
        
        counter += 1  # increment the counter variable
    time.sleep(interval)

cap.release()
