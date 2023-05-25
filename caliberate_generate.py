##########################################################
# generate
##########################################################

import cv2

# camera = cv2.VideoCapture(0)
# camera = cv2.VideoCapture(6) #Top Camera
camera = cv2.VideoCapture(6)
ret, img = camera.read()


path = "/home/sushma/Downloads/Whisker-Robot-Project/chessboard_9_new/"
count = 0
while True:
    name = path + str(count)+".jpg"
    ret, img = camera.read()
    cv2.imshow("img", img)


    if cv2.waitKey(20) & 0xFF == ord('c'):
        cv2.imwrite(name, img)
        cv2.imshow("img", img)
        count += 1
        if cv2.waitKey(0) & 0xFF == ord('q'):
            break