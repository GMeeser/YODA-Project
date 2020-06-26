`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 10.06.2020 16:15:43
// Design Name: 
// Module Name: byte_encrypter
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module byte_encrypter(
    input [7:0] byte_input,
    input [7:0] key,
    input [7:0] counter,
    output [7:0] byte_output
    );
    
    assign byte_output = byte_input^(counter^key);
    
endmodule
