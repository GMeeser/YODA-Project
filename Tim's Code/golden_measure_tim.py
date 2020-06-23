# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 16:27:00 2020

@author: Tim
"""
from PIL import Image

# =============================================================================
# This can take in any image file type in the load_image variable but works best
# with .bmp files. Different file types have different pixel data in each tuple
# which is why the variable number_in_tuple is needed. The key can be changed.
# It'd be interesting to see what the best key to get the most encrypted image
# would be because currently there are artifacts (you can see some detail), but
# this could potentially be eliminated with the right key.
# =============================================================================
# Function to xor bytes. I ended up just using bitwise xor built into python.
def byte_xor(ba1, ba2):
    ba1 = ba1.to_bytes(1,byteorder='big')
    ba2 = ba2.to_bytes(1,byteorder='big')
    return int.from_bytes(bytes([_a ^ _b for _a, _b in zip(ba1, ba2)]), byteorder='big', signed=False)


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
print(len(pix_val_flat))
pix_val_enc = []                                        #List to store the encrypted data
pix_enc = []                                            #List of tuples of encrypted pixels


# Iterate through the 1D list of pixels, xoring with the cypher (key xor counter)
for i in range(0, len(pix_val_flat)):
    xor_key = key^counter                               #xor_key = key xor counter
    enc_pixel = xor_key^pix_val_flat[i]                 #enc_pixel = xor_key xor pix_val_flat[i]
    pix_val_enc.append(enc_pixel)                       #add ecrypted pixel to array
    counter = (counter+1)%256                           #Increment and loop round the counter


# Iterate through the 1D encrypted pixel list and pit the pixels into tuples of 
# size number_in_tuple then puts these into a list
for i in range(0,len(pix_val_flat),number_in_tuple):
    lst = []                                            #temporary list that will be tupled
    #Add the correct number of data points to each tuple. Some image types have RGB some have RGBA etc
    for j in range(0,number_in_tuple):
        lst.append(pix_val_enc[i+j])
        j += 1
    tup = tuple(lst)                                    #Make list into tuple
    pix_enc.append(tup)                                 #Add each tuple to the encrypted pixel list
    
print("Encrypted")                                      #Tells you that it's done encrypting

im2.putdata(pix_enc)                                    #Tell Pillow what the new data for the encrypted image is
im2.save(save_image)                                    #Save the encrypted image