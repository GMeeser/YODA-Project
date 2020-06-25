'''
G. Meeser (grant@meeser.co.za)

25/062020
'''

from PIL import Image
from serial import Serial
import functions

chunk_size = 250

def byte_xor(ba1, ba2):
    # ba1 = ba1.to_bytes(1,byteorder='big')
    # ba2 = ba2.to_bytes(1,byteorder='big')
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

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
com_port = input("Com port to use => ")
#initialise com port
try:
    com = Serial(com_port,timeout=1,baudrate=115200)
except:
    print("Cannot open",com_port)
    exit()

#Golden Meause Key and Offset
golden_key = (inputNumber("KEY (Integer) => ") % 256).to_bytes(1,'big')
golden_offset = (inputNumber("Offset (Integer) => ") % 256).to_bytes(1,'big')

#Load image and convert to flat byte array
try:
    input_image_array, tuple_count = functions.imageToArray(input_image_name)
except:
    print(input_image_name, "cannot be found or is an invalid image.")
    exit()

#Golden Meausre
output_image_array_golden = []
offset = golden_offset
for i in range(0,len(input_image_array)):
    offset = (((int.from_bytes(offset,'big') + i) % 256)).to_bytes(1,'big')
    
    if i % chunk_size == 0:
        offset = golden_offset

    output_image_array_golden.append(byte_xor(input_image_array[i],byte_xor(golden_key,offset)))

#Chunk and send data to FPGA
output_image_array = []
for i in range(0,len(input_image_array),chunk_size):
    com.write(input_image_array[i:i+chunk_size]+b'111')
    output_image_array.append(com.read(chunk_size))

#Check received data against golden measure
for i in range(0,len(input_image_array)):
    if input_image_array[i] != output_image_array[i]:
        raise Exception("Golden measure does not matched recieved data")

print("Recieved data matches golden measure!")

#Rebuild image from byte array
functions.arrayToImage(output_image_array,input_image_name)