import cv2
from cv2 import aruco
import yaml
import numpy as np
from pathlib import Path
from tqdm import tqdm

root = Path(__file__).parent.absolute()

# Set this flag True for calibrating camera and False for validating results real time
calibrate_camera = True

calib_imgs_path = root.joinpath("chessboard_9_new")

# for idx, fn in enumerate(calib_fnms):
#     print(idx, '', end='')
#     img = cv2.imread(str(root.joinpath(fn)))
#     if img is not None:
#         img_list.append(img)
#         h, w, c = img.shape
#     else:
#         print(f"Failed to load image: {fn}")

# For validating results, show aruco board to camera.
aruco_dict = aruco.getPredefinedDictionary( aruco.DICT_6X6_1000 )

#Provide length of the marker's side
markerLength = 3.95#0.95 #3.95 #3.75  # cm ##check looks like 3.9 ish #3.95

# Provide separation between markers
markerSeparation =  0.5#0.15 #0.5   # cm. ##seems right

# create arUco board
board = aruco.GridBoard_create(4, 5, markerLength, markerSeparation, aruco_dict)
# board = aruco.GridBoard_create(4, 2, markerLength, markerSeparation, aruco_dict)


arucoParams = aruco.DetectorParameters_create()

if calibrate_camera == True:
    img_list = []
    calib_fnms = calib_imgs_path.glob('*.jpg')
    print('Using ...', end='')
    for idx, fn in enumerate(calib_fnms):
        print(idx, '', end='')
        img = cv2.imread( str(root.joinpath(fn) ))
        # if img is not None:
        #     img_list.append(img)
        #     h, w, c = img.shape
        # else:
        #     print(f"Failed to load image: {fn}")
        # print("hello")
        img_list.append( img )
        # print("hello2")
        h, w, c = img.shape
        # print("hello3")
    print('Calibration images')

    counter, corners_list, id_list = [], [], []
    first = True
    for im in tqdm(img_list):
        img_gray = cv2.cvtColor(im,cv2.COLOR_RGB2GRAY)
        corners, ids, rejectedImgPoints = aruco.detectMarkers(img_gray, aruco_dict, parameters=arucoParams)
        if first == True:
            corners_list = corners
            id_list = ids
            first = False
        else:
            corners_list = np.vstack((corners_list, corners))
            id_list = np.vstack((id_list,ids))
        counter.append(len(ids))
    print('Found {} unique markers'.format(np.unique(ids)))

    counter = np.array(counter)
    print ("Calibrating camera .... Please wait...")
    ret, mtx, dist, rvecs, tvecs = aruco.calibrateCameraAruco(corners_list, id_list, counter, board, img_gray.shape, None, None )

    print("Camera matrix is \n", mtx, "\n And is stored in calibration11.yaml file along with distortion coefficients : \n", dist)
    data = {'camera_matrix': np.asarray(mtx).tolist(), 'dist_coeff': np.asarray(dist).tolist()}
    with open("calibration11.yaml", "w") as f:
        yaml.dump(data, f)

else:
    camera = cv2.VideoCapture(6) # 0 = laptop webcam; 12 = Front exterior camera; 6 = Top Camera; ? = Interior Camera
    ret, img = camera.read()

    # with open('calibration.yaml') as f: #laptop webcam
    # with open('calibration3.yaml') as f: #Top Camera
    # with open('calibration4.yaml') as f: #Interior Camera
    with open('calibration11.yaml') as f: #front exterior camera
        loadeddict = yaml.load(f)
    mtx = loadeddict.get('camera_matrix')
    dist = loadeddict.get('dist_coeff')
    mtx = np.array(mtx)
    dist = np.array(dist)

    ret, img = camera.read()
    img_gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    h,  w = img_gray.shape[:2]
    newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))

    pose_r, pose_t = [], []
    while True:
        ret, img = camera.read()
        img_aruco = img
        im_gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
        h,  w = im_gray.shape[:2]
        dst = cv2.undistort(im_gray, mtx, dist, None, newcameramtx)
        corners, ids, rejectedImgPoints = aruco.detectMarkers(dst, aruco_dict, parameters=arucoParams)
        if corners == None:
            print ("pass")
        else:

            ret, rvec, tvec = aruco.estimatePoseBoard(corners, ids, board, newcameramtx, dist) # For a board
            print ("Rotation ", rvec, "Translation", tvec)
            if ret != 0:
                img_aruco = aruco.drawDetectedMarkers(img, corners, ids, (0,255,0))
                img_aruco = aruco.drawAxis(img_aruco, newcameramtx, dist, rvec, tvec, 10)    # axis length 100 can be changed according to your requirement

            if cv2.waitKey(0) & 0xFF == ord('q'):
                break
        cv2.imshow("World co-ordinate frame axes", img_aruco)

cv2.destroyAllWindows()

