from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2D, MaxPool2D, Flatten
from keras.utils import np_utils
import tensorflow as tf
import cv2
import numpy as np
import pandas as pd
import os
# from sklearn.preprocessing import LabelEncoder
from sklearn import preprocessing






csv_file = "data_collection.csv"
columns = ['Serial_no.','Timestamp', 'x_actual', 'y_actual', 'direction', 'x_step', 'y_step']
data_df = pd.read_csv(csv_file, header=None, names = columns)

serial_numbers = data_df['Serial_no.'].astype(str).apply(lambda x: int(x.split(',')[0]))

image_folder = "output_images_new"
imagess = []
parsed_custom_info = []

le = preprocessing.LabelEncoder()
data_df['direction'] = le.fit_transform(data_df['direction'])

# for index, info in enumerate(data_df[0]):

for row in data_df.itertuples(index=False, name='Pandas'):
    serial_number = data_df['Serial_no.']
    date_time = data_df['Timestamp']
    x_coordinate = data_df['x_actual']
    y_coordinate = data_df['y_actual']
    direction = data_df['direction']
    x_step = data_df['x_step']
    y_step = data_df['y_step']

    if ~(x_coordinate.empty and y_coordinate.empty):
      # print("Hello")
      for serial_number in serial_numbers:
        image_name = None
        # print("hm")
        for filename in os.listdir(image_folder):
            if filename.startswith(str(serial_number)):
                # print("Hoow is thatt possible")
                image_name = filename
                break
        if image_name is not None:
          # print("I'm HEREEEE")
          image_path = os.path.join(image_folder, image_name)
          image = cv2.imread(image_path)
          image = tf.keras.preprocessing.image.img_to_array(image) ####
          image = image / 255.0 ####
          imagess.append(image)
          images = np.array(imagess) ####

          parsed_custom_info.append([serial_number, date_time, x_coordinate, y_coordinate,  direction, x_step, y_step])