##################  Front Exterior Camera  ################# 

import cv2
import numpy as np
import csv
from datetime import datetime


camera_matrix = np.array([[1361.738, 0, 939.38], [0, 1349.86, 574.198], [0, 0, 1]]) 
dist_coeffs = np.array([-0.23820, 3.6368, -0.003, -0.0076, -16.36])  

# ArUco marker dictionary
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

# Marker size in meters
marker_size = 2.5

# File path to save the coordinates
output_file = 'marker_coordinates_2.csv'

# Function to calculate marker pose
def estimate_marker_pose(marker_corners):
    rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(marker_corners, marker_size, camera_matrix, dist_coeffs)
    return rvecs, tvecs

cap = cv2.VideoCapture(12)

# Open the output file for writing
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Timestamp', 'Marker ID', 'Position (x)', 'Position (y)', 'Position (z)'])

    while True:
        # Read frame from the camera
        ret, frame = cap.read()
        if ret:
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Detect ArUco markers
            corners, ids, _ = cv2.aruco.detectMarkers(gray, aruco_dict)
            # If markers are detected
            if ids is not None:
                rvecs, tvecs = estimate_marker_pose(corners)
                for i in range(len(ids)):
                    # Draw marker outline
                    cv2.aruco.drawDetectedMarkers(frame, corners)
                    # Draw axis for each marker
                    cv2.aruco.drawAxis(frame, camera_matrix, dist_coeffs, rvecs[i], tvecs[i], marker_size * 0.5)
                    # Get real-world coordinates
                    x, y, z = tvecs[i][0]
                    print("Marker ID:", ids[i][0])
                    print("Position (x, y, z):", x, y, z)
                    # Get the current timestamp
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    # Write coordinates to the file
                    writer.writerow([timestamp, ids[i][0], x, y, z])

            cv2.imshow("ArUco Marker Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
