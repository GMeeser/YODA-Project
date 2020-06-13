`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 10.06.2020 16:44:34
// Design Name: 
// Module Name: encrypter_sim
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


module encrypter_sim(

    );
    parameter number_of_bytes = 512;
    
    wire [(number_of_bytes*8)-1:0] output_data;
    wire [(number_of_bytes*8)-1:0] input_data;
    
    wire [7:0] offset = 0;
    
    wire [7:0] key = 0;
    
    bytes_encrypter #(.number_of_bytes(number_of_bytes)) encrypter(.data_in(input_data), .key(key), .offset(offset), .data_out(output_data));
    
endmodule
