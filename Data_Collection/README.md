## Overview


## The code on the Arduino which the x-y plotter is connected to is:
`xy_plotter.ino`

## To view the markers being detected and their information like id run:
`python3 show_marker.py`

## To know which camera is connected to which port run:
`python3 cam_which_port.py`

### Camera 1 (Top Camera)
`python3 real_world_coordinates_cam1.py`  --> get coordinates

### Camera 2 (Front Exterior Camera)
`python3 real_world_coordinates_cam2.py`  --> get coordinates

### Interior Cam
`python3 interior_camprocessor.py`  --> collect membrane images