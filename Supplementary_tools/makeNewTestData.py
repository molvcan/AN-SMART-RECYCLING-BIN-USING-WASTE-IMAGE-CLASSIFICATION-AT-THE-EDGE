'''
Date : 03/27/2022
Author : Xueying Li
Description : This program makes the new test data from my waste data
'''

import os, random
import shutil,math

dataPath = "xueyingsplitall/train/"
newDataPath = "xueyingsplitall/test/"
# The data used for training contains 7 folders, including 5 waste+hand+empty
# The data collected by Jetson nano contains two folders: top and side, and each folder also has the 7 categories
# Train/Test = 90/10
dataseplit=0.15
categories = ["hand","empty","glass","metal","cardboard","paper","plastic"]
# Seperate 15% of the images from each category randomly to form the test set
def makeNewTestData():
    for c in categories:
        oldpathT = dataPath+c+"/"
        # find the total number of data in the path
        fileListT=os.listdir(oldpathT)
        numberofdata=len(fileListT)
        numberoftestdata=math.floor(dataseplit*numberofdata)
        # create directory
        newpathT = newDataPath+c+"/"
        os.mkdir(newpathT)
        for i in range(numberoftestdata):
            img=random.choice(fileListT)
            shutil.copy(oldpathT+img,newpathT+img)
            fileListT.remove(img)
            os.remove(oldpathT+img)

makeNewTestData()
# Combine the "hand" and "empty" with original test set
def combineWithOldTestData():
    # Enter the path of Trashnet test set
    path="OriginalTestEmptyHand/"
    # Make new folders
    os.mkdir(path+"empty/")
    os.mkdir(path+"hand")
    for c in ["empty/","hand/"]:
        count = 1
        for v in ["side/","top/"]:
            fileL = os.listdir(newDataPath+v+c)
            for file in fileL:
                shutil.copy(newDataPath+v+c+file,path+c+str(count)+".jpg")
                count+=1
combineWithOldTestData()

