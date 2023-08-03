import os
import cv2

def crop_center(image_path, crop_width, crop_height):
    image = cv2.imread(image_path)
    height, width, _ = image.shape

    # Calculate the starting point of the crop
    start_x = width // 2 - crop_width // 2
    start_y = height // 2 - crop_height // 2

    # Calculate the ending point of the crop
    end_x = start_x + crop_width
    end_y = start_y + crop_height

    cropped_image = image[start_y:end_y, start_x:end_x]

    return cropped_image


folder_path = 'output_images_new_old'

output_folder = 'cropped_noedges'
os.makedirs(output_folder, exist_ok=True)

# Specify the width and height of the desired crop
crop_width = 1350
crop_height = 1080


for filename in os.listdir(folder_path):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        image_path = os.path.join(folder_path, filename)


        cropped_image = crop_center(image_path, crop_width, crop_height)

        output_path = os.path.join(output_folder, filename)

        cv2.imwrite(output_path, cropped_image)

        ## Display the cropped image
        #cv2.imshow('Cropped Image', cropped_image)
        #cv2.waitKey(0)
print("Completed!")
## Close all windows after processing
#cv2.destroyAllWindows()

