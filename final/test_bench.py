'''
G. Meeser (grant@meeser.co.za)

25/062020
'''

from PIL import Image
from serial import Serial
import functions

chunk_size = 1000

def byte_xor(ba1, ba2):
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

# com_port = input("Com port to use => ")
com_port = '/dev/ttyS4'
#initialise com port
try:
    print("Init COM... ",end="")
    com = Serial(com_port,timeout=10,baudrate=115200)
    print("DONE")
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
print("Producing golden measure... ",end='')
output_image_array_golden = b''
offset = golden_offset
chunk = b''
for i in range(0,len(input_image_array)):
    offset = (((int.from_bytes(offset,'big') + 1) % 256)).to_bytes(1,'big')

    if i % chunk_size+1 == 0 and i > 0:
        offset = golden_offset
        output_image_array_golden = output_image_array_golden + chunk
        chunk = b''
    else:
        chunk = chunk + byte_xor(input_image_array[i].to_bytes(1,'big'),byte_xor(golden_key,offset))
print("DONE")

#Chunk and send data to FPGA
output_image_array = []
print(len(input_image_array), "total Bytes")
print("Sending data to board in chunks of", chunk_size, "Bytes")
for i in range(0,len(input_image_array),chunk_size):
    chunk_array = input_image_array[i:i+chunk_size];
    com.write(chunk_array);
    com.write(bytearray([49]))
    com.write(bytearray([49]))
    com.write(bytearray([49]))
    output_image_array.append(com.read(len(chunk_array)))

#Check received data against golden measure
print("Comparing with golden measure...")
for i in range(0,len(output_image_array_golden)):
    if output_image_array_golden[i] != output_image_array[i]:
        print("Golden measure does not matched recieved data")
        exit()

print("Received data matches golden measure!")

#Rebuild image from byte array
print("Creating output image")
functions.arrayToImage(output_image_array,input_image_name)
print("DONE")
