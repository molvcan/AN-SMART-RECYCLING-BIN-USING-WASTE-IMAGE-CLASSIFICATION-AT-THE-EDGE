'''
Date : 03/27/2022
Author : Xueying Li
Reference: I used part of code from https://github.com/mazabdul7/AtTheEdge/blob/main/main.py
Description : This file includes functions that used to load TensorRT model and use the model 
              to do predictions based on camera input
'''
import tensorflow as tf
import numpy as np
from tensorflow.python.saved_model import signature_constants, tag_constants
from tensorflow.python.framework import convert_to_constants
import time
import cv2

#Change this name to the file name of accelerated model
model_name = 'best224_a'

#Load model
print("Loading Model")
saved_model_loaded = tf.saved_model.load(
    model_name, tags=[tag_constants.SERVING])

#Intantiate graphs from runtime engine
print("Instantiating graph")
graph_func = saved_model_loaded.signatures[signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY]

#Convert graph variables to constants
print("Freezing graph")
graph_func = convert_to_constants.convert_variables_to_constants_v2(
    graph_func)


def inference(input):
	'''Run inference on input'''
	x = tf.constant(np.expand_dims(input, axis=0).astype(np.float32))
	pred = graph_func(x) 
	return pred[0].numpy()[0]

labels = ["cardboard", "glass", "metal", "paper", "plastic"]

def prediction(input):
	predictions = inference(input)
	return predictions
