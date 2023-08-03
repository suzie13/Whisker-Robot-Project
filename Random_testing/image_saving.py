import cv2 

cam = cv2.VideoCapture(8)
output_path = 'Random_testing_images/10.jpg' 

while True:
    # Capture a frame from the camera
    ret, frame = cam.read()

    # Check if the frame was captured successfully
    if not ret:
        print("Error: Unable to capture frame.")
        break

    # cv2.imshow('Camera', frame)
    cv2.imwrite(output_path, frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()



