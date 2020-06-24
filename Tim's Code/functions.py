# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 16:28:15 2020

@author: Tim
"""
from PIL import Image


def imageToArray(im_file):
    im = Image.open(im_file)
    #List of Tuples
    pix_val = list(im.getdata())
    number_in_tuple = len(pix_val[0])
    #1D list
    pix_val_flat = [x for sets in pix_val for x in sets]
    #To access use pix_val_flat, number_in_tuple = imageToArray(the_image.bmp)
    return pix_val_flat, number_in_tuple

def arrayToImageArray(encrypted_array, number_in_tuple):
    for i in range(0,len(encrypted_array),number_in_tuple):
        #Temporary list that will be tupled
        lst = []
        #Encrypted List
        encrypted_image_array = []                                            
        #Add the correct number of data points to each tuple. Some image types have RGB some have RGBA etc
        for j in range(0,number_in_tuple):
            lst.append(encrypted_array[i+j])
            j += 1
        #Make list into tuple
        tup = tuple(lst)
        #Add each tuple to the encrypted pixel list
        encrypted_image_array.append(tup)                                 
        
    return(encrypted_image_array)

def arrayToImage(encrypted_image_array,unencrypted_image_file,image_file_to_be_saved):
    im = Image.open(unencrypted_image_file)
    #Make second image same size as first
    im2 = Image.new(im.mode, im.size)
    #Load pixle data into image
    im2.putdata(encrypted_image_array)
    #Save Image
    im2.save(image_file_to_be_saved)