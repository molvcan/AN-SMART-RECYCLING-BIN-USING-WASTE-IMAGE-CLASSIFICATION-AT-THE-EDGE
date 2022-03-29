import RPi.GPIO as GPIO
import time
# the data pin of IR sensor is connected to pin 16
'''
Date : 03/27/2022
Author : Xueying Li
Description : This file includes functions that sets pin model on 
              the board and reads input from an IR sensor
'''
# Pin 16 is connected to the output pin of the IR sensor
inputPin = 16
# Use Board pin numbering scheme
GPIO.setmode(GPIO.BOARD)
# Set this pin as input pin
GPIO.setup(inputPin,GPIO.IN)

# Ask  IR sensor if the people present
def isPeoplePresent(): 
     # GPIO.LOW when people present,HIGH when not present
    value =GPIO.input(inputPin)
    if (value == GPIO.HIGH):
        print("high")
        return False
    else: 
        print("low")
        return True
# Clean up the settings after the application is exited
def cleanup():
    GPIO.cleanup()

