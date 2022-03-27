'''
Date : 03/27/2022
Author : Xueying Li
Description : This program resize all the training data into a smaller size such as 224x224 pixels
'''
from PIL import Image
from os import listdir

foldername= "xueyingsplitall224"
# resize all the training data into 224x224 pixels for K210 training
for f in listdir(foldername):
    path =foldername+"/"+f
    for file in listdir(path):
        for im in listdir(path+'/'+file):
            image = Image.open(path+'/'+file+"/"+im)
            image= image.resize((224,224))
            image.save(path+'/'+file+"/"+im, image.format)
