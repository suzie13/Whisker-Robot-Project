from time import perf_counter

# First import the library
import pyrealsense2 as rs
# Import Numpy for easy array manipulation
import numpy as np
# Import OpenCV for easy image rendering
import cv2
import argparse


# Create a pipeline
pipeline = rs.pipeline()

# Create a config and configure the pipeline to stream
#  different resolutions of color and depth streams
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

found_rgb = False
for s in device.sensors:
    if s.get_info(rs.camera_info.name) == 'RGB Camera':
        found_rgb = True
        break
if not found_rgb:
    print("The demo requires Depth camera with Color sensor")
    exit(0)

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

if device_product_line == 'L500':
    config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
else:
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
#profile = pipeline.start(config)
cfg = pipeline.start(config)



# Getting the depth sensor's depth scale (see rs-align example for explanation)
#depth_sensor = profile.get_device().first_depth_sensor()
depth_sensor = cfg.get_device().first_depth_sensor()

depth_scale = depth_sensor.get_depth_scale()
print("Depth Scale is: " , depth_scale)

# We will be removing the background of objects more than
#  clipping_distance_in_meters meters away
clipping_distance_in_meters = 1 #1 meter
clipping_distance = clipping_distance_in_meters / depth_scale

# Create an align object
# rs.align allows us to perform alignment of depth frames to others frames
# The "align_to" is the stream type to which we plan to align depth frames.
align_to = rs.stream.color
align = rs.align(align_to)

max_value = 255
max_value_H = 360//2
low_H = 0
low_S = 0
low_V = 0
high_H = max_value_H
high_S = max_value
high_V = max_value
window_capture_name = 'Video Capture'
window_detection_name = 'Object Detection'
low_H_name = 'Low H'
low_S_name = 'Low S'
low_V_name = 'Low V'
high_H_name = 'High H'
high_S_name = 'High S'
high_V_name = 'High V'
lh=110
uh=130

def on_low_H_thresh_trackbar(val):
    global low_H
    global high_H
    low_H = val
    low_H = min(high_H-1, low_H)
    cv2.setTrackbarPos(low_H_name, window_detection_name, low_H)
def on_high_H_thresh_trackbar(val):
    global low_H
    global high_H
    high_H = val
    high_H = max(high_H, low_H+1)
    cv2.setTrackbarPos(high_H_name, window_detection_name, high_H)
def on_low_S_thresh_trackbar(val):
    global low_S
    global high_S
    low_S = val
    low_S = min(high_S-1, low_S)
    cv2.setTrackbarPos(low_S_name, window_detection_name, low_S)
def on_high_S_thresh_trackbar(val):
    global low_S
    global high_S
    high_S = val
    high_S = max(high_S, low_S+1)
    cv2.setTrackbarPos(high_S_name, window_detection_name, high_S)
def on_low_V_thresh_trackbar(val):
    global low_V
    global high_V
    low_V = val
    low_V = min(high_V-1, low_V)
    cv2.setTrackbarPos(low_V_name, window_detection_name, low_V)
def on_high_V_thresh_trackbar(val):
    global low_V
    global high_V
    high_V = val
    high_V = max(high_V, low_V+1)
    cv2.setTrackbarPos(high_V_name, window_detection_name, high_V)
parser = argparse.ArgumentParser(description='Code for Thresholding Operations using inRange tutorial.')
parser.add_argument('--camera', help='Camera divide number.', default=0, type=int)
args = parser.parse_args()

#cv2.namedWindow(window_capture_name)
#cv2.namedWindow(window_detection_name)
#cv2.createTrackbar(low_H_name, window_detection_name , low_H, max_value_H, on_low_H_thresh_trackbar)
#cv2.createTrackbar(high_H_name, window_detection_name , high_H, max_value_H, on_high_H_thresh_trackbar)
#cv2.createTrackbar(low_S_name, window_detection_name , low_S, max_value, on_low_S_thresh_trackbar)
#cv2.createTrackbar(high_S_name, window_detection_name , high_S, max_value, on_high_S_thresh_trackbar)
#cv2.createTrackbar(low_V_name, window_detection_name , low_V, max_value, on_low_V_thresh_trackbar)
#cv2.createTrackbar(high_V_name, window_detection_name , high_V, max_value, on_high_V_thresh_trackbar)
# Streaming loop

try:
    while True:
    
        # Get frameset of color and depth
        frames = pipeline.wait_for_frames()
        # frames.get_depth_frame() is a 640x360 depth image

        # Align the depth frame to color frame
        aligned_frames = align.process(frames)

        # Get aligned frames
        aligned_depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image
        color_frame = aligned_frames.get_color_frame()

        # Validate that both frames are valid
        if not aligned_depth_frame or not color_frame:
            continue

        depth_image = np.asanyarray(aligned_depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Remove background - Set pixels further than clipping_distance to grey
        grey_color = 153
        depth_image_3d = np.dstack((depth_image,depth_image,depth_image)) #depth image is 1 channel, color is 3 channels
        bg_removed = np.where((depth_image_3d > clipping_distance) | (depth_image_3d <= 0), grey_color, color_image)

       
        hsv = cv2.cvtColor(bg_removed, cv2.COLOR_BGR2HSV)

       
        lower_purple = np.array([lh,50,50])
        upper_purple= np.array([uh,250,250])
     
        mask = cv2.inRange(hsv, lower_purple, upper_purple)
       
        res = cv2.bitwise_and(bg_removed,bg_removed, mask= mask)



        #frame_HSV = cv2.cvtColor(hsv, cv.COLOR_BGR2HSV)
        frame_threshold = cv2.inRange(hsv, (low_H, low_S, low_V), (high_H, high_S, high_V))

        img1 = color_image
        img2 = res
        rows,cols,channels = res.shape
        roi = img1[0:rows, 0:cols]
        mask_inv = cv2.bitwise_not(mask)

        #img = cv2.imread(color_image)
        #kernel = np.ones((5,5),np.uint8)
        #erosion = cv2.erode(res,kernel,iterations = 1)
        #opening = cv2.morphologyEx(res, cv2.MORPH_OPEN, kernel)
        #cv2.imshow('erosion', erosion)
        #img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)

        #img2_fg = cv2.bitwise_and(img2,img2,mask = mask)
        #dst = cv2.add(img1_bg,img2_fg)
        #img1[0:rows, 0:cols ] = dst

        contours,hierarchy = cv2.findContours(mask, 1, 2)
        cx=0
        cy=0
    
        if len(contours)!=0:
    
            areas = [cv2.contourArea(c) for c in contours]
            #print(f"areas={areas}")
            max_idx = np.argmax(areas)
            cnt = contours[max_idx]
            #cnt = contours[0]
            M = cv2.moments(cnt)
            #print( M )
            #while(M['m00']!=0):
            if M['m00']>0 :
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                print((cx, cy))
            

            #perimeter = cv2.arcLength(cnt,True)

            
        cv2.drawContours(res, contours, -1, (0,255,0), 3)
        cv2.circle(res, (cx, cy), 7, (255, 255, 255), -1)
        cv2.drawContours(color_image, contours, -1, (0,255,0), 3)
        cv2.circle(color_image, (cx, cy), 7, (0, 255, 255), -1)
        #dpt_frame = pipeline.wait_for_frames().get_depth_frame().as_depth_frame()
        dpt_frame = aligned_depth_frame.as_depth_frame()
        pixel_distance_in_meters = dpt_frame.get_distance(cx,cy)
        #print(pixel_distance_in_meters)

        #cfg = pipeline.start(config) # Note in the example code, cfg is misleadingly called "profile" but cfg is a better name
        profile = cfg.get_stream(rs.stream.color)
        intr = profile.as_video_stream_profile().get_intrinsics()
        centroid=rs.rs2_deproject_pixel_to_point(intr,[cx,cy],pixel_distance_in_meters)

        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        images = np.hstack((res,color_image))

        cv2.namedWindow('Align Example', cv2.WINDOW_NORMAL)
        cv2.imshow('Align Example', images)

        #cv2.imshow(window_capture_name, res)
        #cv2.imshow(window_detection_name, frame_threshold)

        #cv2.imshow('mask_inv',mask_inv)

        key = cv2.waitKey(1)
        # Press esc or 'q' to close the image window
        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break
finally:
    pipeline.stop()
