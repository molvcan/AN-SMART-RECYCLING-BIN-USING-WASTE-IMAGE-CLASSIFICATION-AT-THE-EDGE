'''
Date : 03/27/2022
Author : Xueying Li
Description : This file is used to collect training data. Execute this file and press "q" to take photos.
'''


import capture
import cv2
import os

# Change the name of category to save the image in different folders
category ="empty"
def saveImage(path,img):
    isNamed=False
    count=1
    # go through the files in the folder to avoid same name
    while isNamed==False:
        file = path+str(count)+".jpg"
        if os.path.isfile(file)==False:
            isNamed = True
            cv2.imwrite(file,img)
        count+=1
try:
    while(1):
        img0 = capture.capture_input0()
        img1 = capture.capture_input1()
        cv2.imshow("img0",img0)
        cv2.imshow("img1",img1)
        if cv2.waitKey(1)==ord('q'):
            saveImage("CollectedTraindata/top"+"/"+category+"/",img0)
            saveImage("CollectedTraindata/side"+"/"+category+"/",img1)
        if cv2.waitKey(1)==ord('c'):
            break
finally :
    capture.release()
