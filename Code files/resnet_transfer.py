#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import os
import tensorflow as tf
import cv2
#from tensorflow import keras
#from tensorflow.keras import layers, models
#from tensorflow.keras.regularizers import l2


IMG_WIDTH=150
IMG_HEIGHT=150
IMG_SIZE = (150, 150)
img_folder=r'/home/meghna1/train_data/'
label_mapping_fair_face={0:['White'],1:['Black'],2:['Southeast Asian','East Asian'],3:['Indian'],4:['Latino_Hispanic','Middle Eastern'],5:['Cartoon'],6:['Cat'],7:['Dog']}

def create_dataset(img_folder):
    file_count=0
    img_data_array=[]
    class_name=[]
    labels={}
    with open('/home/meghna1/fairface_label_train.csv','r') as label_file:
        for line in label_file:
            lines=line.split(',')
            if lines[0]!='file':
                file_no=lines[0].split('/')[1].split('.')[0]
                labels[file_no]=lines[3]
    for dir1 in os.listdir(img_folder):
        for file in os.listdir(os.path.join(img_folder, dir1)):
            file_count+=1
#            print(file_count)
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
                class_name.append(6)
            elif dir1=='Dog':
                class_name.append(7)
    return img_data_array, class_name


# In[ ]:


train_data,train_labels =create_dataset(img_folder)
train_data=np.asarray(train_data)
train_data.shape


# In[ ]:


train_labels=np.asarray(train_labels).reshape(len(train_labels),1)
train_data = train_data.reshape(train_data.shape[0], 150, 150, 3)
train_labels=tf.keras.utils.to_categorical(
    train_labels, num_classes=8, dtype='float32'
)


# In[ ]:


from tensorflow import keras
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras import layers,models
from tensorflow.keras import optimizers


# In[ ]:


IMG_SHAPE = IMG_SIZE + (3,)
base_model = tf.keras.applications.resnet50.ResNet50(weights= None, include_top=False, input_shape= IMG_SHAPE)
base_model.trainable = False
base_model.summary()


# In[ ]:


feature_batch = base_model(train_data)
global_average_layer = tf.keras.layers.GlobalAveragePooling2D()
feature_batch_average = global_average_layer(feature_batch)
print(feature_batch_average.shape)


# In[ ]:


prediction_layer = tf.keras.layers.Dense(1)
prediction_batch = prediction_layer(feature_batch_average)
print(prediction_batch.shape)


# In[ ]:


data_augmentation = tf.keras.Sequential([
  tf.keras.layers.experimental.preprocessing.RandomFlip('horizontal'),
  tf.keras.layers.experimental.preprocessing.RandomRotation(0.2),
])
preprocess_input = tf.keras.applications.resnet50.preprocess_input


# In[ ]:


inputs = tf.keras.Input(shape=(150, 150, 3))
x = data_augmentation(inputs)
x = preprocess_input(x)
x = base_model(x, training=False)
x = global_average_layer(x)
x = tf.keras.layers.Dropout(0.2)(x)
outputs = prediction_layer(x)
model = tf.keras.Model(inputs, outputs)


# In[ ]:


opt=tf.keras.optimizers.Adam(learning_rate=0.0001)
model.compile(optimizer=opt,
              loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])


# In[ ]:


model.summary()


# In[ ]:


history = model.fit(train_data,train_labels, batch_size=64,epochs=50,validation_split=0.25)


# In[ ]:


acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

# plt.figure(figsize=(8, 8))
# plt.subplot(2, 1, 1)
# plt.plot(acc, label='Training Accuracy')
# plt.plot(val_acc, label='Validation Accuracy')
# plt.legend(loc='lower right')
# plt.ylabel('Accuracy')
# plt.ylim([min(plt.ylim()),1])
# plt.title('Training and Validation Accuracy')

# plt.subplot(2, 1, 2)
# plt.plot(loss, label='Training Loss')
# plt.plot(val_loss, label='Validation Loss')
# plt.legend(loc='upper right')
# plt.ylabel('Cross Entropy')
# plt.ylim([0,1.0])
# plt.title('Training and Validation Loss')
# plt.xlabel('epoch')
# plt.show()

