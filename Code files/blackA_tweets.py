import gzip
import glob
import json

path='/Users/Meghna/Desktop/Filtered_BlackA_Tweets/*.json.gz'

files=glob.glob(path)
len_f=0
for i in range(len(files)):
    print("opening file", files[i])
    file_name=files[i].split("/")[-1]
    try:
        with gzip.open(files[i],'r') as fin:
            for line in fin:
                len_f+=1
    except:
        print("Faulty file ", files[i])
        
print(len_f) #len_f=618