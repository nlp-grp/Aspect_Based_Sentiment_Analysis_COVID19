import pandas as pd
import numpy as np
import os
import tensorflow as tf
import cv2
import pathlib
#from tensorflow import keras
from tensorflow.keras import layers, models

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
import pickle
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import pickle
from PIL import Image
import numpy as np

IMG_WIDTH=150
IMG_HEIGHT=150
img_folder=r'/data/meghna1/train_data/'
label_mapping_fair_face={0:['White','Southeast Asian','Indian','Latino_Hispanic','Middle Eastern','East Asian'],1:['Black']}

def create_dataset(img_folder):
    file_count=0
    img_data_array=[]
    class_name=[]
    labels={}
    
    #counting the number of examples in each class, goal is to have equal number of example for
    #african amercians vs others. The others class also has different subclasses
    count_aa = 0
    count_white = 0
    count_sa = 0
    count_ind = 0
    count_lat = 0
    count_mid = 0
    count_ea = 0
    count = 0
    
    # getting image labels from imag elabel file
    with open('/data/meghna1/fairface_label_train.csv','r') as label_file:
        for line in label_file:
            lines=line.split(',')
            if lines[0]!='file':
                file_no=lines[0].split('/')[1].split('.')[0]
                labels[file_no]=lines[3]

    #loading data
    for dir1 in os.listdir(img_folder):
        if dir1 == 'train':
            for file in os.listdir(os.path.join(img_folder, dir1)):
                file_count+=1
                image_path= os.path.join(img_folder, dir1,  file)
                file_num=file.split('.')[0]
                for k,v in label_mapping_fair_face.items():
                    if labels[file_num] in v:
                        if labels[file_num] == 'Black' and count_aa <12233:
                            class_name.append(k)
                            count_aa += 1
                            image= cv2.imread( image_path, cv2.COLOR_BGR2RGB)
                            image=np.array(image)
                            image = image.astype('float32')
                            #image /= 255 
                            image=cv2.resize(image, (IMG_HEIGHT, IMG_WIDTH),interpolation = cv2.INTER_AREA)
                            img_data_array.append(image)
                        elif labels[file_num] == 'White' and count_white <2039 and count<12233:
                            class_name.append(k)
                            count_white += 1
                            count += 1
                            image= cv2.imread( image_path, cv2.COLOR_BGR2RGB)
                            image=np.array(image)
                            image = image.astype('float32')
                            #image /= 255 
                            image=cv2.resize(image, (IMG_HEIGHT, IMG_WIDTH),interpolation = cv2.INTER_AREA)
                            img_data_array.append(image)
                        elif labels[file_num] == 'Southeast Asian' and count_sa <2039 and count<12233:
                            class_name.append(k)
                            count_sa += 1
                            count += 1
                            image= cv2.imread( image_path, cv2.COLOR_BGR2RGB)
                            image=np.array(image)
                            image = image.astype('float32')
                            #image /= 255 
                            image=cv2.resize(image, (IMG_HEIGHT, IMG_WIDTH),interpolation = cv2.INTER_AREA)
                            img_data_array.append(image)
                        elif labels[file_num] == 'Indian' and count_ind <2039 and count<12233:
                            class_name.append(k)
                            count_ind += 1
                            count += 1
                            image= cv2.imread( image_path, cv2.COLOR_BGR2RGB)
                            image=np.array(image)
                            image = image.astype('float32')
                            #image /= 255 
                            image=cv2.resize(image, (IMG_HEIGHT, IMG_WIDTH),interpolation = cv2.INTER_AREA)
                            img_data_array.append(image)
                        elif labels[file_num] == 'Latino_Hispanic' and count_lat <2039 and count<6000:
                            class_name.append(k)
                            count_lat += 1
                            count += 1
                            image= cv2.imread( image_path, cv2.COLOR_BGR2RGB)
                            image=np.array(image)
                            image = image.astype('float32')
                            #image /= 255 
                            image=cv2.resize(image, (IMG_HEIGHT, IMG_WIDTH),interpolation = cv2.INTER_AREA)
                            img_data_array.append(image)
                        elif labels[file_num] == 'Middle Eastern' and count_mid <2039 and count<12233:
                            class_name.append(k)
                            count_mid += 1
                            count += 1
                            image= cv2.imread( image_path, cv2.COLOR_BGR2RGB)
                            image=np.array(image)
                            image = image.astype('float32')
                            #image /= 255 
                            image=cv2.resize(image, (IMG_HEIGHT, IMG_WIDTH),interpolation = cv2.INTER_AREA)
                            img_data_array.append(image)
                        elif labels[file_num] == 'East Asian' and count_ea <203 and count<12233:
                            class_name.append(k)
                            count_ea += 1
                            count += 1
                            image= cv2.imread( image_path, cv2.COLOR_BGR2RGB)
                            image=np.array(image)
                            image = image.astype('float32')
                            #image /= 255 
                            image=cv2.resize(image, (IMG_HEIGHT, IMG_WIDTH),interpolation = cv2.INTER_AREA)
                            img_data_array.append(image)
    return img_data_array, class_name


train_data,train_labels =create_dataset(img_folder)

train_data=np.asarray(train_data)

train_labels=np.asarray(train_labels).reshape(len(train_labels),1)

train_data = train_data.reshape(train_data.shape[0], 150, 150, 3)

bluec = []
greenc = []
redc = []
#     blue.append(b)
#     green.append(g)
#     red.append(r)
new_x_train = []

for i in range(len(train_data)):
    blue,green,red = cv2.split(train_data[i])
    blue_temp_df = pd.DataFrame(data = blue)
    green_temp_df = pd.DataFrame(data = green)
    red_temp_df = pd.DataFrame(data = red)
    df_blue = blue/255
    df_green = green/255
    df_red = red/255
    pca_b = PCA(n_components=0.95)
    pca_b.fit(df_blue)
    trans_pca_b = pca_b.transform(df_blue)
    pca_g = PCA(n_components=0.95)
    pca_g.fit(df_green)
    trans_pca_g = pca_g.transform(df_green)
    pca_r = PCA(n_components=0.95)
    pca_r.fit(df_red)
    trans_pca_r = pca_r.transform(df_red)
    bluec.append(trans_pca_b.shape[1])
    greenc.append(trans_pca_r.shape[1])
    redc.append(trans_pca_g.shape[1])
    b_arr = pca_b.inverse_transform(trans_pca_b)
    g_arr = pca_g.inverse_transform(trans_pca_g)
    r_arr = pca_r.inverse_transform(trans_pca_r)
    img_reduced= (cv2.merge((b_arr, g_arr, r_arr)))
    data = np.array(img_reduced)
    flattened = data.flatten()
    new_x_train.append(flattened)
    
    
# splitting data into train and validation data
from sklearn.model_selection import train_test_split
x_train, x_validate,y_train,y_validate = train_test_split(new_x_train,train_labels,test_size=0.25, random_state = 1)


clf = SVC(kernel='rbf', class_weight='balanced',C=100)
clf = clf.fit(x_train, y_train)

y_pred = clf.predict(x_validate)
print(classification_report(y_validate, y_pred, target_names=classes))


file_path = '/data/meghna1/svm_images_rgb'
pickle.dump(clf, open(file_path, 'wb'))
    