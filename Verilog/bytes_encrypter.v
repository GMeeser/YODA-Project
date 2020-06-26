`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 13.06.2020 11:10:11
// Design Name: 
// Module Name: bytes_encrypter
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


module bytes_encrypter
    #(  
        parameter number_of_bytes = 256
     )
     (
        input wire [((number_of_bytes*8)-1):0] data_in,
        input wire [7:0] key,
        input wire [7:0] offset,
        output wire [((number_of_bytes*8)-1):0] data_out
    );
    
    genvar gi;
    
    generate
        for (gi=0; gi < number_of_bytes; gi=gi+1) begin
            byte_encrypter single_byte(.byte_input(data_in[(gi*8)+7:(gi*8)]), .key(key), .counter((offset+gi)%256), .byte_output(data_out[(gi*8)+7:(gi*8)]));
        end
    endgenerate
endmodule
