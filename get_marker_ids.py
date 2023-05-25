import cv2
from cv2 import aruco
import numpy as np
import time

class MarkSearch :

    dict_aruco = aruco.Dictionary_get(aruco.DICT_4X4_50)
    parameters = aruco.DetectorParameters_create()

    def __init__(self, cameraID):
        self.cap = cv2.VideoCapture(cameraID)

    def get_markID(self):
        #Obtain marker id list from still image
        ret, frame = self.cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, dict_aruco, parameters=parameters)

        list_ids = np.ravel(ids)

        return list_ids

 
if __name__ == "__main__" :
    import cv2
    from cv2 import aruco
    import numpy as np
    import time

    dict_aruco = aruco.Dictionary_get(aruco.DICT_4X4_50)
    parameters = aruco.DetectorParameters_create()

    #parameter
    # cameraID = 0
    cameraID = 6
    cam0_mark_search = MarkSearch(cameraID)

    try:
        while True:
            print(' ----- get_markID ----- ')
            print(cam0_mark_search.get_markID())
            time.sleep(0.5)
    except KeyboardInterrupt:
        cam0_mark_search.cap.release()
