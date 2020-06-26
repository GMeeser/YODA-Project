`timescale 1ns / 1ps

module top(
    input wire CLK100MHZ,
    input wire UART_TXD_IN,
    input wire [15:0] SW,
    output wire UART_RXD_OUT,
    output reg [15:0] LED
    );

    SerialEncrypter encrypter(.i_clk(CLK100MHZ), .o_uart_tx(UART_RXD_OUT), .i_uart_rx(UART_TXD_IN), .i_switches(SW));

    always @(posedge CLK100MHZ) begin
        // turn on LED for whichever switch is turned on
        LED <= SW;
    end

endmodule
