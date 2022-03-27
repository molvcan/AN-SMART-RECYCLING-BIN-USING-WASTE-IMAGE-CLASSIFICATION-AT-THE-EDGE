'''
Date : 03/27/2022
Author : Xueying Li
Description : This program makes the training data by combining the collected new data with odld data
'''
import os, random
import shutil
# with the old data. It copies data from new data path to all data path
allDataPath = "xueyingsplitall/train/"

# Change this path to change the position of new data
newDataPath = "AllTrainingData/"

# The data used for training contains 7 folders, including 5 waste+hand+empty
# The data collected by Jetson nano contains two folders: top and side, and each folder also has the 7 categories
# The code copy the data collected by Jetson nano to the folder of the data used for training
categories = ["glass","metal","cardboard","paper","plastic","hand","empty"]
os.mkdir(allDataPath+"empty/")
os.mkdir(allDataPath+"hand/")
for c in categories:
    fileList =os.listdir(allDataPath+c+"/")
    count = len(fileList)+1
    for v in ["top/","side/"]:
        fileL = os.listdir(newDataPath+v+c+"/")
        for file in fileL:
            shutil.copy(newDataPath+v+c+"/"+file,allDataPath+c+"/"+str(count)+".jpg")
            count+=1

