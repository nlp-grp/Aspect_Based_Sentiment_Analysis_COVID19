img_folder=r'/Users/Meghna/Desktop/check/'
import os
import cv2
import numpy as np
img_data_array=[]
label_mapping_fair_face={0:'White',1:'Black',2:'Southeast Asian, East Asian',3:'Indian',4:'Latino_Hispanic, Middle Eastern'}
for dir1 in os.listdir(img_folder):
    if dir1=='.DS_Store':
        continue
    else:
        for file in os.listdir(os.path.join(img_folder, dir1)):
            image_path= os.path.join(img_folder, dir1,  file)
            image= cv2.imread( image_path, cv2.COLOR_BGR2RGB)
            #image=cv2.resize(image, (IMG_HEIGHT, IMG_WIDTH),interpolation = cv2.INTER_AREA)
            image=np.array(image)
            image = image.astype('float32')
            image /= 255
            img_data_array.append(image)
            file_num=file.split('.')[0]

            with open('/Users/Meghna/Desktop/fairface_label_train.csv','r') as label_file:
                    for line in label_file:
                        lines=line.split(',')
                        if lines[0]!='file' and lines[0].split('/')[1].split('.')[0]==file_num:
                            for k,v in label_mapping_fair_face.items():
                                if label_mapping_fair_face[k]==lines[3]:
                                    print(k," ", v, " ", lines[3])
