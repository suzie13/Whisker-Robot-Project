# Whisker-Robot-Project
![first](https://github.com/suzie13/Whisker-Robot-Project/assets/39700209/7551480b-d7f8-43c4-b751-79352ac690ce)

<br>

## Setup Measurements Diagram

![Adobe Scan May 11, 2023_1](https://github.com/suzie13/Whisker-Robot-Project/assets/39700209/69407845-7a0c-4218-a413-b3a4ca2041a9)


## Project Setup

![IMG_1684](https://github.com/suzie13/Whisker-Robot-Project/assets/39700209/dcb398b5-f4dd-4efc-a855-afd3717f94ad)

<br>

## Top View

![IMG_20230511_132359](https://github.com/suzie13/Whisker-Robot-Project/assets/39700209/b3e1111f-b002-4003-93bc-bd74bef94cc9)

## Interior Camera View
![membrane](https://github.com/suzie13/Whisker-Robot-Project/assets/39700209/be6ac9f2-6f29-4a2f-b720-d957197e6b58)


## Front Exterior Camera View

![Screenshot from 2023-05-11 13-23-19](https://github.com/suzie13/Whisker-Robot-Project/assets/39700209/642cb324-06f6-4bbd-949f-13828b590804)

![Screenshot from 2023-05-10 19-42-01](https://github.com/suzie13/Whisker-Robot-Project/assets/39700209/48aedbd8-3197-4e83-a09e-d9b8ac97ae29)

<br>

## Output from show_marker.py for Front Cam and Top Cam

![Screenshot from 2023-05-25 03-02-28](https://github.com/suzie13/Whisker-Robot-Project/assets/39700209/1f79e9df-57e9-401e-aa24-b2130fa43ee8)


![Screenshot from 2023-05-24 20-24-10](https://github.com/suzie13/Whisker-Robot-Project/assets/39700209/c87a5836-ffa0-457b-9dae-0f267173b760)



## Output from real_world_coordinates_cam1.py 

![Screenshot from 2023-05-23 21-35-02](https://github.com/suzie13/Whisker-Robot-Project/assets/39700209/393ff659-fecd-456b-9fd4-af9a6bea8683)


<br>
<br>

## To start the Automatic Data Collection run
`python3 automatic_data_collection.ipynb`

This above includes everything that is required to perform automatic data collection; like connect to the Arduino serial port, 
show markers, check which camera is what number i.e which port it is connected to. <br> In a nutshell, all the required standalone 
codes from the Data Collection folder for automatic data collection, are used as functions in this code. <br>
<br>
<br>
<br>

# Overview
<br>
<ul> -> The "caliberation" folder contains everything that is required to procure the camera matrix and distance coefficient 
values which is used in Data Collection for aruco marker detection. <br> It also contains code to generate aruco marker images. </ul> <br>
<ul> -> The "Data_Collection" folder contains all the standalone codes used in the automatic data collection process.    </ul> <br>
<ul> -> The "helper_functions" folder is for codes that can be handy for various tasks. <br>
It contains crop.py file which is used to crop images, such that the dimensions (of part of the image to keep) <br>
are taken from the center. This was used to see if edges (in membrane images) played a role in the model learning.
Turns out edges did play a role. </ul> <br>
<ul> -> The "ML_algos" folder contains all the machine learning algorithms used in this project. </ul> <br>
<br>
<br>


## Portfolio Link for Whisker Robot project!:
https://suzie13.github.io/Sushma_S_Chandra/projects/Whisker%20Robot/
