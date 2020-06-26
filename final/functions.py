# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 16:28:15 2020

@author: Tim
"""
from PIL import Image

def byteArrayToIntegerArray(byte_array):
    integer_array = []
    for i in byte_array:
        y = [x for x in i]
        if (len(integer_array) != 0):
            integer_array.extend(y)
        else:
            integer_array = y
    return integer_array

def imageToArray(im_file):
    im = Image.open(im_file)
    #List of Tuples
    pix_val = list(im.getdata())
    number_in_tuple = len(pix_val[0])
    #1D list
    pix_val_flat = [x for sets in pix_val for x in sets]
    return pix_val_flat, number_in_tuple

def arrayToImageArray(encrypted_array, number_in_tuple):
    encrypted_array = byteArrayToIntegerArray(encrypted_array)
    #Encrypted List
    encrypted_image_array = []
    for i in range(0,len(encrypted_array),number_in_tuple):
        #Temporary list that will be tupled
        lst = []
        #Add the correct number of data points to each tuple. Some image types have RGB some have RGBA etc
        for j in range(0,number_in_tuple):
            lst.append(encrypted_array[i+j])
        #Make list into tuple
        tup = tuple(lst)
        #Add each tuple to the encrypted pixel list
        encrypted_image_array.append(tup)

    return(encrypted_image_array)

def arrayToImage(encrypted_image_array,unencrypted_image_file):
    #Open Original image to get size and colour depth
    im = Image.open(unencrypted_image_file)
    #Make second image same size as first
    im2 = Image.new(im.mode, im.size)
    #Convert byte array to image data array
    encrypted_image_array = arrayToImageArray(encrypted_image_array, len(im.mode))
    #Load pixle data into image
    im2.putdata(encrypted_image_array)
    #Save Image
    name_array = unencrypted_image_file.split(".")
    im2.save(".".join(name_array[:-1])+"_encrypted."+name_array[-1])
