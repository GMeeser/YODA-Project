# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 09:55:25 2020

@author: Tim
"""

import time
import serial
from PIL import Image

#Process image into list
load_image = "darth.bmp"                                #Image to be encrypted
save_image = "darth-enc.bmp"                            #Image to be saved
key = 204                                               #The encryption key. Change this to change the encryption
counter = 0                                             #Counter starts at 0 and loops round at 255

im = Image.open(load_image)                             #Opens the image
im2 = Image.new(im.mode, im.size)                       #Creates the image that will be saved in the same dimensions as the old image
pix_val = list(im.getdata())                            #Makes a list of tuples containing the pixel RGB data
width, height = im.size                                 #Gets the image dimensions
number_in_tuple = len(pix_val[0])                       #Allows for different size tuples depending on the image file type
pix_val_flat = [x for sets in pix_val for x in sets]    #Makes the pixel data into a 1D list


# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='COM3',
    baudrate=115200,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

ser.isOpen()

print('Enter your commands below.\r\nInsert "image" to send image.\r\nInsert a string to send a string.\r\nInsert "exit" to leave the application.')

while 1 :
    # get keyboard input
    x = input()
        # Python 3 users
        # input = input(">> ")
    if x == 'exit':
        ser.close()
        exit()
    if x == 'image':
        #Send 4 byte start signal
        start_bytes = 'strt'
        start_bytes = start_bytes.encode()
        ser.write(start_bytes)
        out = []
        # let's wait one second before reading output (let's give device time to answer)
        time.sleep(1)
        while ser.inWaiting() > 0:
            out.append(ser.read(1))

        if out != []:
            print(out)
        #Send 256 bytes of pixels to board
        pix_val_flat_temp = pix_val_flat
        more_pixels = True                 #If more_pixels is True there are more pixels to be sent
        while more_pixels:
            if len(pix_val_flat_temp)<257:
                send_string = (''.join(str(x) for x in pix_val_flat_temp)).encode()
                ser.write(send_string)
                more_pixels = False
                out = []
                # let's wait one second before reading output (let's give device time to answer)
                time.sleep(1)
                while ser.inWaiting() > 0:
                    out.append(ser.read(1))
        
                if out != []:
                    print(out)
            else:
                pix_send = pix_val_flat_temp[0:257]
                send_string = (''.join(str(x) for x in pix_val_flat_temp)).encode()
                ser.write(send_string)
                pix_val_flat_temp = pix_val_flat_temp[257:]
                out = []
                # let's wait one second before reading output (let's give device time to answer)
                time.sleep(1)
                while ser.inWaiting() > 0:
                    out.append(ser.read(1))
        
                if out != []:
                    print(out)
            
            
            
    else:
        # send the character to the device
        values = x.encode()
        ser.write(values)
        ser.write(bytearray([13]))
        out = []
        # let's wait one second before reading output (let's give device time to answer)
        time.sleep(1)
        while ser.inWaiting() > 0:
            out.append(ser.read(1))

        if out != []:
            print(out)
                
