# YODA-Project Data Encryption Accelerator
Code repositor for Yoda project UCT EEE4120F - 2020 parallel encrypter

This project focused on the implementation of a Data Encryption Accelerator(DEA). The purpose of a DEA is to accelerate the encryption of a stream of data. The encryption method used is a simple XOR encryption, but the security of the encryption is improved by making use of a key and a counter to produce the cyper. The encryption takes place on the Nexys A7 FPGA board. The data to be encrypted is sent to the board via the serial port. A key is input by the user using the 8 bit data in bus. The data is then encrypted and sent back to the laptop.

The encryption used takes the equation form DATA_OUT = XOR(DATA_IN,XOR(Key,Counter)). This is achieved by XORing the used input key with the counter and then XORing this with the data. The counter increments after each byte and counts up to 255 before looping back.

