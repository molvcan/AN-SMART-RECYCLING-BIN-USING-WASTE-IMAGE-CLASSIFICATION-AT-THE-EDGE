﻿'''
Date : 03/27/2022
Author : Xueying Li
Description : Run this program to start the AI bin application. It uses the functions in other three programs.
              Two cammeras are used to do the classfication.
'''
#################################################################################
#Logic flow:
#black screen 
#↓ 
#determine whether IR input is LOW  → HIGH： back to black screen
# ↓
#LOW: Start inference,take photo, display photo, classifying → HAND : wait, continue classifying
#↓
#OTHER: display the result on the screen, ask the user correct or not →CORRECT : store the result, throw rubbish, back to the start
#↓
#WRONG: ask the user to input correct result, store the result, throw rubbish, and back to the start

#################################################################################
import tkinter
import RPi.GPIO as GPIO
import time
import cv2
from PIL import Image, ImageTk
import os
import capture
import inference
import IR
import tensorflow as tf
import numpy as np
from tensorflow.python.saved_model import signature_constants, tag_constants
from tensorflow.python.framework import convert_to_constants
#################################################################################
#Functions

# Read from IR sensor untill there is people detected
def continueDetecting(display): 
    isDetected =False
    while isDetected ==False:
        time.sleep(0.5)
        isDetected =IR.isPeoplePresent()
    classfication(display)

# Call camera to take photos, it would return an image
def camera(): 
    # Use the function in capture.py to initialize camera and take photos
    img0 = capture.capture_input0()
    img1 = capture.capture_input1()
    return [img0,img1]

# Convert the img from np.array format to the format used by tkinter
def convertImage(img):
    img = cv2.cvtColor(img ,cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img =  ImageTk.PhotoImage(image=img)
    return img

# Display the photos taken on the canvas
def displayImageOnCanvas(display, app,img0,img1):
    img0 = convertImage(img0)
    img1 = convertImage(img1)
    # Display the top view
    display.create_image(0, 0, anchor=tkinter.NW, image=img0)
    display.create_image(512, 0, anchor=tkinter.NW, image=img1)
    # Update the canvas to display the photos
    app.update_idletasks()
    app.update()
# Start the inference and call the model to classify the photos
# The photos will be classified into 7 groups
def most_frequent(List):
    count= 0
    element = 0
    for i in List: 
        frequency = List.count(i)
        if frequency >count:
            count = frequency
            element = i
    return element
def classiyPrediction(predictions,output,predictions1,output1,labels=):
    if output in [1,3] and  predictions[output]*100 > 30:
        prediction = labels[output]
    if predictions[output]*100 > 99 :
        prediction = labels[output]
    elif predictions1[output1]*100>99 :
        prediction = labels[output1]
    else:
        prediction="unknown"
    return prediction

def classfication(display):
    labels=["cardboard", "empty","glass","hand", "metal", "paper", "plastic"]
    count=0
    queue = [0]
    queue1= [0]
    queueLen=40
    while True:
        [img,img1]=camera()
        displayImageOnCanvas(display,app,img,img1)
        predictions =inference.prediction(img)
        output = np.argmax(predictions)
        predictions1 =inference.prediction(img1)
        output1 = np.argmax(predictions1)
        print(output,output1)
        if len(queue)<queueLen:
            queue.append(output)
            queue1.append(output1)
        else:
            break
    output = most_frequent(queue)
    output1 = most_frequent(queue1)
    prediction=classiyPrediction(predictions,output,predictions1,output1,labels)
    Label=None
    var =None
    # wait until the camera detected object
    while True:
        # if there is no object in the box
        if var ==None:
            var = tkinter.StringVar()
        if prediction == "empty":
            var.set("Empty")
        # if the user is holding the object
        elif prediction =="hand":
            var.set("Hand present\nPlease put the rubbish there and remove your hand")
        elif prediction =="unknown":
            var.set("Can not detect anything,please put the waste in the centre")
        else:
            # once the detection is not hand or empty, get out of the loop
            time.sleep(0.1)
            break
        if Label==None:
            Label = tkinter.Label(app,
                                       textvariable = var,
                                       fg="black",bg="white",justify="left",anchor="e",pady=50,font=("Arial",25))
            Label.pack()
        displayImageOnCanvas(display,app,img,img1)
        time.sleep(0.01)
        [img,img1]= camera() #Top image and side image
        starttime=time.time()
        predictions =inference.prediction(img)
        output = np.argmax(predictions)
        endtime = time.time()
        print(endtime-starttime)
        predictions1 =inference.prediction(img1)
        output1 = np.argmax(predictions1)
        print(output,output1)
        queue.pop(0)
        queue.append(output)
        queue1.pop(0)
        queue1.append(output1)
        output = most_frequent(queue)
        output1 = most_frequent(queue1)
        print( predictions[output],predictions1[output1])
        prediction=classiyPrediction(predictions,output,predictions1,output1,labels)
        previousPrediction=predictions
    if Label!=None:
        Label.destroy()
    askIfCorrect(display,prediction,img,img1)


# Ask the user if the prediction is correct or not
def askIfCorrect(display,prediction,img0,img1):
    # destory the canvas of previous stage
    display.destroy()
    displayText = "I detected "+prediction+"\nIs this correct?"
    # print result and ask if it is correct
    ResultLabel = tkinter.Label(app, 
                                       text = displayText,justify="left",
                                       fg="black",bg="white",padx=100,pady=100,font=("Arial",25))
    ResultLabel.pack()
    # Make two buttons, right and wrong
    # clear all the widgets created
    def cleanFrame():
        ResultLabel.destroy()
        correctButton.destroy()
        wrongButton.destroy()
    # if the user says the result is correct
    def correct():
        path="EdgeDataset11"
        saveImage(path+"/top/"+prediction+"/",img0)
        saveImage(path+"/side/"+prediction+"/",img1)
        cleanFrame()
        thankYou()
    # if the user says the result is wrong
    def wrong():
        cleanFrame()
        askForCorrection(img0,img1)
    # create the two buttons and put them onto the window
    correctButton=tkinter.Button(app,text="correct",command =correct,font=("Arial",25))
    correctButton.pack()
    wrongButton=tkinter.Button(app,text="wrong",command =wrong,font=("Arial",25))
    wrongButton.pack()

# Call the motor to move the rubbish into the container
def throwRubbish():
    print("This function will call the motor")
    #Make sure your hand is away, the machine will start to operat

# print thank you at the end 
def thankYou():
    displayText="thankyou!\nPlease put you hand away,\n I am going move the rubbish into the container"
    thankLabel = tkinter.Label(app, 
                                       text = displayText,justify="left",
                                       fg="black",bg="white",font=("Arial",25))
    thankLabel.pack()
    throwRubbish()
    # return to the start page
    def after():
        thankLabel.destroy()
        loopEvent()    
    thankLabel.after(5000,after)
    

# Save image after classification
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

# If the user saysthe classification is wrong, 
# this function will ask the correct group
def askForCorrection(img0,img1):
    Foldername = "EdgeDataset11"
    # Clean the frame
    def destroyAll():
        askLabel.destroy()
        paperButton.destroy()
        cardboardButton.destroy()
        metalButton.destroy()
        plasticButton.destroy()
        glassButton.destroy()
        thankYou()
    # Save the image into the folder of the group corrected by the user
    def paper():
        path=Foldername
        saveImage(path+"/top/"+"paper/",img0)
        saveImage(path+"/side/"+"paper/",img1)
        destroyAll()
    def cardboard():
        path=Foldername
        saveImage(path+"/top/"+"cardboard/",img0)
        saveImage(path+"/side/"+"cardboard/",img1)
        destroyAll()
    def metal():
        path=Foldername 
        saveImage(path+"/top/"+"metal/",img0)
        saveImage(path+"/side/"+"metal/",img1)
        destroyAll()
    def plastic():
        path=Foldername 
        saveImage(path+"/top/"+"plastic/",img0)
        saveImage(path+"/side/"+"plastic/",img1)
        destroyAll()
    def glass():
        path=Foldername 
        saveImage(path+"/top/"+"glass/",img0)
        saveImage(path+"/side/"+"glass/",img1)
        destroyAll()
    # display the question and the buttons
    askLabel = tkinter.Label(app, 
                                       text ="Oh,sorry. Which is the correct category?",justify="left",
                                       fg="black",bg="white",padx=100,pady=100,font=("Arial",25))
    askLabel.pack()
    paperButton=tkinter.Button(app,text="Paper",command=paper,font=("Arial",25))
    paperButton.pack()
    cardboardButton=tkinter.Button(app,text="Cardboard",command =cardboard,font=("Arial",25))
    cardboardButton.pack()
    metalButton=tkinter.Button(app,text="Metal",command =metal,font=("Arial",25))
    metalButton.pack()
    plasticButton=tkinter.Button(app,text="Plastic",command =plastic,font=("Arial",25))
    plasticButton.pack()
    glassButton=tkinter.Button(app,text="Glass",command =glass,font=("Arial",25))
    glassButton.pack()

# This function loops the classification program
def loopEvent():
    display = tkinter.Canvas(app,bg='black',width=1024,height=384)
    display.pack(side="top")
    def continueD():
        continueDetecting(display)
    app.after(10000,continueD)

    

#################################################################################

try:
    app = tkinter.Tk()
    #app.attributes('-fullscreen', True)#set to full screen
    app.geometry("1024x600")
    app.configure(bg='white')
    app.title('Waste Classification Programme') # set the name of the window
    # Start the main program which is a loop event
    loopEvent()
    app.mainloop()
finally:
    IR.cleanup()
    capture.release()

