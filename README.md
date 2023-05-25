# Whisker-Robot-Project


![Screenshot from 2023-05-04 15-12-48](https://user-images.githubusercontent.com/39700209/236318854-19b883a5-861f-48e9-bd5c-a984d1751342.png)



## Interior Camera View
![image_0](https://user-images.githubusercontent.com/39700209/236319310-ef87984c-bbc2-4645-8a92-429ef181f9a2.jpg)


## Project Setup

![IMG_20230511_132530](https://github.com/suzie13/Whisker-Robot-Project/assets/39700209/cef4c361-4bcb-4727-ab46-828a7d5c4f02)



## Top View

![IMG_20230511_132359](https://github.com/suzie13/Whisker-Robot-Project/assets/39700209/b3e1111f-b002-4003-93bc-bd74bef94cc9)


## Setup Measurements Diagram

![Adobe Scan May 11, 2023_1](https://github.com/suzie13/Whisker-Robot-Project/assets/39700209/69407845-7a0c-4218-a413-b3a4ca2041a9)



## Front Exterior Camera View

![Screenshot from 2023-05-11 13-23-19](https://github.com/suzie13/Whisker-Robot-Project/assets/39700209/642cb324-06f6-4bbd-949f-13828b590804)

![Screenshot from 2023-05-10 19-42-01](https://github.com/suzie13/Whisker-Robot-Project/assets/39700209/48aedbd8-3197-4e83-a09e-d9b8ac97ae29)


## Output from show_marker.py for Front Cam and Top Cam

![Screenshot from 2023-05-25 03-02-28](https://github.com/suzie13/Whisker-Robot-Project/assets/39700209/1f79e9df-57e9-401e-aa24-b2130fa43ee8)

![Screenshot from 2023-05-25 03-00-30](https://github.com/suzie13/Whisker-Robot-Project/assets/39700209/d63b08b4-455d-4610-bf00-a627179d9566)

![Screenshot from 2023-05-24 20-24-10](https://github.com/suzie13/Whisker-Robot-Project/assets/39700209/c87a5836-ffa0-457b-9dae-0f267173b760)



## Output from real_world_coordinates_cam1.py 

![Screenshot from 2023-05-23 21-35-02](https://github.com/suzie13/Whisker-Robot-Project/assets/39700209/393ff659-fecd-456b-9fd4-af9a6bea8683)



## Command to run multiple files in parallel/ to sync cameras/data collection: ####



# Making use of GNU Parallel command-line tool
# sudo apt-get install parallel

# Camera 1 (Top Camera)
python3 real_world_coordinates_cam1.py  #get coordinates

# Camera 2 (Front Exterior Camera)
python3 real_world_coordinates_cam2.py  #get coordinates

# Interior Cam
python3 interior_camprocessor.py  #collect images

# To sync data collection from all three cameras
parallel -j 3 python3 ::: real_world_coordinates_cam1.py real_world_coordinates_cam2.py interior_camprocessor.py


### 3 stands for 3 jobs to start simultaneosly/ run concurrently
