# Overview
<br>
<br>

## Arduino Code 
`xy_plotter.ino`  --> The code on the Arduino which the x-y plotter is connected to. <br>
<br>

## View aruco markers
`python3 show_marker.py`  --> To view the markers being detected and their information like id. Also, check the view from camera. <br>
<br>

## Camera Ports 
`python3 cam_which_port.py`  --> To know which camera is connected to which port <br>
<br>

## Camera 1 (Top Camera)
`python3 real_world_coordinates_cam1.py`  --> get coordinates <br>
<br>

## Camera 2 (Front Exterior Camera)
`python3 real_world_coordinates_cam2.py`  --> get coordinates <br>
<br>

## Interior Cam
`python3 interior_camprocessor.py`  --> collect membrane images <br>

<br>
<br>
<br>

# Supplementary
<br>
<br>

## Whisker & Object point of contact using Computer Vision only
`python3 point_of_contact.py`  --> initial code to find point of contact of object to whisker using pure Computer Vision (no aruco markers <br> or Machine Learning). If the distance between two contours is lower than a certain threshold then it is considered as touching (in contact).<br>
<br>

## Centroid of object contours
`python3 realsense_camprocessor.py`  --> find countours of object based on color threshold and find its centroid (was used in an earlier <br> project [Who stole my Pen?]) Link: https://suzie13.github.io/Sushma_S_Chandra/projects/Track_and_Grab_a_Pen/  <br>
<br>

## xy plotter control using python commands
`python3 xyplotter_save.ipynb`  --> simple serial port connection; moving x-y plotter using python commands. <br>

