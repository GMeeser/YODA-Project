# YODA-Project Data Encryption Accelerator
## Code repositor for Yoda project UCT EEE4120F - 2020 parallel encrypter

This project focused on the implementation of a Data Encryption Accelerator(DEA). The purpose of a DEA is to accelerate the encryption of a stream of data. The encryption method used is a simple XOR encryption, but the security of the encryption is improved by making use of a key and a counter to produce the cyper. The encryption takes place on the Nexys A7 FPGA board. The data to be encrypted is sent to the board via the serial port. A key is input by the user using the 8 bit data in bus. The data is then encrypted and sent back to the laptop.

The encryption used takes the equation form DATA_OUT = XOR(DATA_IN,XOR(Key,Counter)). This is achieved by XORing the used input key with the counter and then XORing this with the data. The counter increments after each byte and counts up to 255 before looping back.

![Block Diagram](/block_diagram.png)

## Usage
### FPGA setup
Verilog files for this project can be found in /Verilog/ If you would like to recreate this project follow the following steps:
1. Create a new Vivado Project for the Nexys A7
2. Add all .v files to your project making top.v the top file
3. Add the constraint file found in Verilog/constraints
4. Generate bitstream and program board

### running the testbench
Running the testbench is fairly simple. follow the steps below:
1. take note of the serial port your board is connected to
2. identify the image you'd like to encrypt (there are some example images under /images)
3. run 'pip3 install -r requirements.txt' to to install python dependancies
4. run 'python3 test_bench' and supply the relative path to the image you would like to encrypt along with the key and offset that are set on the board.
5. the encrypted image will be output to the same directory as the input image with "-encrypted" appended to its name
