
# ### Overlay marker ID and video ###
import cv2
from cv2 import aruco
import time

dict_aruco = aruco.Dictionary_get(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters_create()

cap = cv2.VideoCapture(8) # Front Exterior Camera
# cap = cv2.VideoCapture(6) # Top Camera 


try:
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, dict_aruco, parameters=parameters)

        frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
        cv2.imshow('frame', frame_markers)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyWindow('frame')
    cap.release()
except KeyboardInterrupt:
    cv2.destroyWindow('frame')
    cap.release()

###################################

# import numpy as np

# all_camera_idx_available = []

# for camera_idx in range(10):
#     cap = cv2.VideoCapture(camera_idx)
#     if cap.isOpened():
#         print(f'Camera index available: {camera_idx}')
#         all_camera_idx_available.append(camera_idx)
#         cap.release()