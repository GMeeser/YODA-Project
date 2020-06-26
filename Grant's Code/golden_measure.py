from PIL import Image
import time
import functions

chunk_size = 2048

def byte_xor(ba1, ba2):
    return (int.from_bytes(ba1,'big')^int.from_bytes(ba2,'big')).to_bytes(1,'big')

def inputNumber(message):
  while True:
    try:
       userInput = int(input(message))       
    except ValueError:
       print("Not an integer! Try again.")
       continue
    else:
       return userInput 
       break 

#Get image and COM port data from user
input_image_name = input("Path to image to use => ")

#Golden Measure Key and Offset
golden_key = (inputNumber("KEY (Integer) => ") % 256).to_bytes(1,'big')
golden_offset = (inputNumber("Offset (Integer) => ") % 256).to_bytes(1,'big')

#Load image and convert to flat byte array
try:
    input_image_array, tuple_count = functions.imageToArray(input_image_name)
except:
    print(input_image_name, "cannot be found or is an invalid image.")
    exit()

#Golden Meausre
print("Producing golden measure... ",end='')
tic = time.time()
output_image_array_golden = b''
offset = golden_offset
chunk = b''
for i in range(0,len(input_image_array)):
    
    if (i % (chunk_size) == 0) and (i > 0):
        offset = golden_offset

    output_image_array_golden = output_image_array_golden + byte_xor(input_image_array[i],byte_xor(golden_key,offset))
    
    offset = (((int.from_bytes(offset,'big') + 1) % 256)).to_bytes(1,'big')

print("DONE")
print("Time Taken:", (time.time()-tic),"seconds")

#Rebuild image from byte array
functions.arrayToImage(output_image_array_golden,input_image_name)