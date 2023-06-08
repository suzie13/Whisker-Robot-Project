import cv2
import numpy as np
import csv
from datetime import datetime

# Default values for direction and x-step
direction_default = "left"
x_step_default = 200

camera_matrix = np.array([[682.694, 0, 573.5379], [0, 675.82, 367.535], [0, 0, 1]])
dist_coeffs = np.array([-0.119, 0.1449, 0.0019, -0.00689, -0.1701])

# ArUco marker dictionary
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

# Marker size in meters
marker_size = 2.6  # or 2.61

# File path to save the coordinates
output_file = 'marker_coordinates_1.csv'

# Function to calculate marker pose
def estimate_marker_pose(marker_corners):
    rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(marker_corners, marker_size, camera_matrix, dist_coeffs)
    return rvecs, tvecs

cap = cv2.VideoCapture(0)

# Open the output file for writing
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Updated header row to include direction and x-step columns
    writer.writerow(['Timestamp', 'Marker ID', 'Position (x)', 'Position (y)', 'Position (z)', 'direction', 'x-step'])

    # Prompt the user to input direction and x-step values
    direction = input("Enter the direction (default: left): ") or direction_default
    x_step = input("Enter the x-step (default: 200): ") or x_step_default

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
                    # Write coordinates to the file along with direction and x-step values
                    writer.writerow([timestamp, ids[i][0], x, y, z, direction, x_step])

            cv2.imshow("ArUco Marker Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
