# # Camera calibration parameters
# # camera_matrix = np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]])
# # dist_coeffs = np.array([k1, k2, p1, p2, k3])
# # camera_matrix = np.array([[1.36, 0, 9.39], [0, 1.349, 5.74], [0, 0, 1]]) 
# # dist_coeffs = np.array([-2.3, 3.63, -3.03, -7.61, -1.63])  
# # Front Exterior Camera 
# # camera_matrix = np.array([[1361.738, 0, 939.38], [0, 1349.86, 574.198], [0, 0, 1]]) 
# # dist_coeffs = np.array([-0.23820, 3.6368, -0.003, -0.0076, -16.36])  
# # Top Camera
# # camera_matrix = np.array([[6269.871, 0, 306.4394], [0, 3657.5737, 637.492], [0, 0, 1]]) 
# # dist_coeffs = np.array([5.73639, -1152.3162, 0.2011, 0.374, 44370.0546])  
# #below one is better than above
# # camera_matrix = np.array([[918.486, 0, 391.392], [0, 696.456, 628.5421], [0, 0, 1]]) 
# # dist_coeffs = np.array([0.262573, -0.7287, 0.03564, 0.0277, 3.3808]) 
# #smaller but up close (not good results)
# # camera_matrix = np.array([[2314.979, 0, 367.628], [0, 2853.8849, 641.341], [0, 0, 1]]) 
# # dist_coeffs = np.array([-1.6349, 30.666, 0.069194, 0.04119, -230.776]) 
# #10yaml good close ish
# camera_matrix = np.array([[682.694, 0, 573.5379], [0, 675.82, 367.535], [0, 0, 1]]) 
# dist_coeffs = np.array([-0.119, 0.1449, 0.0019, -0.00689, -0.1701]) 


#############################################################################

import cv2
import numpy as np
import csv
from datetime import datetime

camera_matrix = np.array([[682.694, 0, 573.5379], [0, 675.82, 367.535], [0, 0, 1]]) 
dist_coeffs = np.array([-0.119, 0.1449, 0.0019, -0.00689, -0.1701]) 

# ArUco marker dictionary
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

# Marker size in meters
marker_size = 2.6  # or 2.61

# File path to save the coordinates
output_file = 'marker_coordinates2.csv'

# Function to calculate marker pose
def estimate_marker_pose(marker_corners):
    rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(marker_corners, marker_size, camera_matrix, dist_coeffs)
    return rvecs, tvecs

cap = cv2.VideoCapture(6)

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
