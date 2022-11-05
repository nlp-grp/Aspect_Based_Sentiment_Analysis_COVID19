import pandas as pd
import numpy as np
import os
import tensorflow as tf
import cv2
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.models import Sequential, Model
from  matplotlib import pyplot as plt
import matplotlib.image as mpimg


IMG_WIDTH=200
IMG_HEIGHT=200
img_folder=r'/Users/Meghna/Desktop/train_data/'
label_mapping_fair_face={0:'White',1:'Black',2:'Southeast Asian, East Asian',3:'Indian',4:'Latino_Hispanic, Middle Eastern'}
def create_dataset(img_folder):

    img_data_array=[]
    class_name=[]

    for dir1 in os.listdir(img_folder):
        if dir1=='.DS_Store':
            continue
        else:
            for file in os.listdir(os.path.join(img_folder, dir1)):
                image_path= os.path.join(img_folder, dir1,  file)
                image= cv2.imread( image_path, cv2.COLOR_BGR2RGB)
                #image=cv2.resize(image, (IMG_HEIGHT, IMG_WIDTH),interpolation = cv2.INTER_AREA)
                # image=np.array(image)
                # image = image.astype('float32')
                # image /= 255
                # img_data_array.append(image)
                if dir1=='UTKFace' or dir1=='crop_part1':
                    race=file.split('_')[2]
                    class_name.append(race)
                else:
                    file_num=file.split('.')[0]
                    with open('/Users/Meghna/Desktop/fairface_label_train.csv','r') as label_file:
                        for line in label_file:
                            lines=line.split(',')
                            if lines[0]!='file' and lines[0].split('/')[1].split('.')[0]==file_num:
                                for k,v in label_mapping_fair_face.items():
                                    if label_mapping_fair_face[k]==lines[3]:
                                        class_name.append(lines[3])
                                        #print(k," ", v, " ", lines[3])

    return img_data_array, class_name

img_data, class_name =create_dataset(img_folder)

#target_dict={k: v for v, k in enumerate(np.unique(class_name))}

#target_val=  [target_dict[class_name[i]] for i in range(len(class_name))]

model=tf.keras.Sequential(
        [
            tf.keras.layers.InputLayer(input_shape=(IMG_HEIGHT,IMG_WIDTH, 3)),
            tf.keras.layers.Conv2D(filters=32, kernel_size=3, strides=(2, 2), activation='relu'),
            tf.keras.layers.Conv2D(filters=64, kernel_size=3, strides=(2, 2), activation='relu'),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(5)
        ])
encoder.compile(optimizer='rmsprop', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

history = model.fit(x=np.array(img_data, np.float32), y=np.array(list(map(int,target_val)), np.float32), epochs=50)
