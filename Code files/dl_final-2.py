import pandas as pd
import numpy as np
import os
import tensorflow as tf
import cv2
import pathlib
from tensorflow.keras import layers, models


IMG_WIDTH=150
IMG_HEIGHT=150
img_folder=r'train_data_folder'
label_mapping_fair_face={0:['White'],1:['Black'],2:['Southeast Asian','East Asian'],3:['Indian'],4:['Latino_Hispanic','Middle Eastern'],5:['Cartoon','Cat','Dog']}

def create_dataset(img_folder):
    file_count=0
    img_data_array=[]
    class_name=[]
    labels={}
    with open('fairface_train_data_path','r') as label_file:
        for line in label_file:
            lines=line.split(',')
            if lines[0]!='file':
                file_no=lines[0].split('/')[1].split('.')[0]
                labels[file_no]=lines[3]
    for dir1 in os.listdir(img_folder):
        try:
            for file in os.listdir(os.path.join(img_folder, dir1)):
                file_count+=1
                image_path= os.path.join(img_folder, dir1,  file)
                image= cv2.imread( image_path, cv2.COLOR_BGR2RGB)
                image=np.array(image)
                image = image.astype('float32')
                image /= 255
                image=cv2.resize(image, (IMG_HEIGHT, IMG_WIDTH),interpolation = cv2.INTER_AREA)
                img_data_array.append(image)
                if dir1=='train':
                    file_num=file.split('.')[0]
                    for k,v in label_mapping_fair_face.items():
                        if labels[file_num] in v:
                            class_name.append(k)
                elif dir1=='UTKFace' or dir1=='crop_part1':
                    caption=file.split("_")
                    if len(caption)!=4:
                        race=caption[1]
                    else:
                        race=caption[2]
                    class_name.append(int(race))
                elif dir1=='cartoon':
                    class_name.append(5)
                elif dir1=='Cat':
                    class_name.append(5)
                elif dir1=='Dog':
                    class_name.append(5)
        except:
            continue
    return img_data_array, class_name

train_data,train_labels =create_dataset(img_folder)

train_data=np.asarray(train_data)

train_labels=np.asarray(train_labels).reshape(len(train_labels),1)

train_data = train_data.reshape(train_data.shape[0], 150, 150, 3)

train_labels=tf.keras.utils.to_categorical(
    train_labels, num_classes=8, dtype='float32'
)

from sklearn.model_selection import train_test_split
x_train, x_validate,y_train,y_validate = train_test_split(train_data,train_labels,stratify=train_labels,test_size=0.25)


model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', padding='same',input_shape=(150,150,3)))
model.add(layers.Conv2D(32, (3, 3), activation='relu'))
model.add(layers.Conv2D(32, (3, 3), activation='relu'))
model.add(layers.Conv2D(32, (3, 3), activation='relu'))
model.add(layers.Dropout(0.25))
#model.add(layers.Conv2D(32, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.BatchNormalization())
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.Dropout(0.25))
#model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.BatchNormalization())
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.Conv2D(128, (3, 3), activation='relu', padding='same'))
model.add(layers.Conv2D(128, (3, 3), activation='relu', padding='same'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.BatchNormalization())
model.add(layers.Flatten())
model.add(layers.Dense(128, activation='relu',kernel_regularizer=tf.keras.regularizers.l2(0.0001)))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(512, activation='relu',kernel_regularizer=tf.keras.regularizers.l2(0.0001)))
model.add(layers.Dense(8,activation='softmax'))

opt=tf.keras.optimizers.Adam(learning_rate=0.0001)

model.compile(optimizer=opt,
              loss=tf.keras.losses.CategoricalCrossentropy(),
              metrics=['accuracy'])

history = model.fit(train_data,train_labels, batch_size=16,epochs=75,validation_data=(x_validate,y_validate))

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

print(acc)
print("------------")
print(val_acc)
print("------------")
print(loss)
print("------------")
print(val_loss)
print("------------")
