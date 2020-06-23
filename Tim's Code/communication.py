# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 15:48:01 2020

@author: Tim
"""
import serial

# =============================================================================
# I was just copy pasting a couple of the bytes from the encoding algorithm 
# into where it says ser.write(b'AT') in place of the AT part. 
# Obviously there is a much more streamlined way to do it, but this was whipped
# up in a couple of minutes just to check that Grant's board sends stuff back. 
# You'll probably have to format the stuff from the FPGA so it can be decoded
# to check the image is correct.
# =============================================================================

with serial.Serial('COM3',timeout=10,baudrate=115200) as ser:
    
    print(ser.name)         #Check which port was really used
    ser.write(b'Hello World')        #The AT command gets back OK from Grant's board
    x = ser.read(100)       #This says how many characters are expected to be read back (so cuts off end characters)
    print(x)                #This checks what you got back
    ser.close()             # close port
    print("closed")         #To check it's done
