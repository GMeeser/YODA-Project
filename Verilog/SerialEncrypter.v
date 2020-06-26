module	SerialEncrypter(i_clk,
			i_setup,
i_uart_rx, i_switches, o_uart_tx);
	input wire		i_clk;
	input	[30:0]	i_setup;
	input wire		i_uart_rx;
	input wire [15:0] i_switches;
	output	wire	o_uart_tx;

	// If i_setup isnt set up as an input parameter, it needs to be set.
	// We do so here, to a setting appropriate to create a 115200 Baud
	// comms system from a 100MHz clock.  This also sets us to an 8-bit
	// data word, 1-stop bit, and no parity.
	wire	[30:0]	i_setup;
	assign		i_setup = 31'd868;	// 115200 Baud, if clk @ 100MHz

    parameter number_of_bytes = 1024;


    // Initialise buffers and their 1D representations
	reg	[7:0]	inBuffer[0:number_of_bytes-1];
	reg [7:0]   outBuffer[0:number_of_bytes-1];

	reg [8*number_of_bytes-1:0] inBuffer_1D;
    wire [8*number_of_bytes-1:0] outBuffer_1D;

    // pointer variables
	reg	[10:0]	head, tail;
	wire	[10:0]	nxt_head;
	reg	[10:0]	lineend;

	// get key and offset from switches
	wire [7:0] offset = i_switches[7:0];
    wire [7:0] key = i_switches[15:8];

    // map 2D buffer to 1D wire
    integer j;
    integer i;
    always @(*) begin
        for (i=0; i<number_of_bytes; i=i+1) begin
            inBuffer_1D[(8*i)+:8] <= inBuffer[i];
        end
        for (j=0; j<number_of_bytes;j=j+1) begin
            outBuffer[j] <= outBuffer_1D[(8*j)+:8];
        end
    end

	// initialise encryptor
	bytes_encrypter #(.number_of_bytes(number_of_bytes)) encrypter(.data_in(inBuffer_1D), .key(key), .offset(offset), .data_out(outBuffer_1D));

	// Create a reset line that will always be true on a power on reset
	reg	pwr_reset;
	initial	pwr_reset = 1'b1;
	always @(posedge i_clk)
		pwr_reset <= 1'b0;

	// The UART Receiver
	//
	// This is where everything begins, by reading data from the UART.
	//
	// Data (rx_data) is present when rx_stb is true.  Any parity or
	// frame errors will also be valid at that time.  Finally, we'll ignore
	// errors, and even the clocked uart input distributed from here.
	wire	rx_stb, rx_break, rx_perr, rx_ferr;
	wire	rx_ignored;
	wire	[7:0]	rx_data;

    // initialise receiver
	rxuart	receiver(i_clk, pwr_reset, i_setup, i_uart_rx, rx_stb, rx_data,
			rx_break, rx_perr, rx_ferr, rx_ignored);


	// The next step in this process is to dump everything we read into a
	// FIFO.  First step: writing into the FIFO.  Always write into FIFO
	// memory.  (The next step will step the memory address if rx_stb was
	// true ...)

	assign	nxt_head = head + 8'h01;
	always @(posedge i_clk)
	    inBuffer[head] <= rx_data;

	// Select where in our FIFO memory to write.  On reset, we clear the
	// memory.  In all other cases/respects, we step the memory forward.
	//
	// However ... we won't step it forward IF ...
	//	rx_break	- we are in a BREAK condition on the line
	//		(i.e. ... it's disconnected)
	//	rx_perr		- We've seen a parity error
	//	rx_ferr		- Same thing for a frame error
	//	nxt_head != tail - If the FIFO is already full, we'll just drop
	//		this new value, rather than dumping random garbage
	//		from the FIFO until we go round again ...  i.e., we
	//		don't write on potential overflow.
	//
	// Adjusting this address will make certain that the next write to the
	// FIFO goes to the next address--since we've already written the FIFO
	// memory at this address.

	initial	head= 8'h00;
	always @(posedge i_clk)
		if ((pwr_reset))
			head <= 8'h00;
		else if ((rx_stb)&&(!rx_break)&&(!rx_perr)&&(!rx_ferr)&&(nxt_head != tail))
			head <= nxt_head;
		else if (tail == lineend) begin
			// Line buffer has been emptied
			head <= 8'h00;
        end

	reg		run_tx;

	// Here's the guts of the algorithm--setting run_tx.
	// Once the line has been transmitted
	// we stop transmitting.
	initial	run_tx = 0;
	initial	lineend = 1;
	always @(posedge i_clk)
		if (pwr_reset)
		begin
			run_tx <= 1'b0;
			lineend <= 8'h01;
        end else if((inBuffer[head]==8'h31) && (inBuffer[head-1]==8'h31) && (inBuffer[head-2]==8'h31)&&(rx_stb))
		begin
			// Start transmitting once we get the end string
			lineend <= head-8'h2;
			run_tx <= 1'b1;
		end else if (tail == lineend) begin
			// Line buffer has been emptied
			run_tx <= 1'b0;
        end
	// Now ... let's deal with the transmitter
	wire	tx_break, tx_busy;
	assign	tx_break = 1'b0;
	reg	[7:0]	tx_data;
	reg		tx_stb;

	// transmit when run_tx is true--but we'll give it an extra clock.
	initial	tx_stb = 1'b0;
	always @(posedge i_clk)
		tx_stb <= run_tx;

	// We'll transmit the data from our FIFO from wherever our tail
	// is pointed.
	always @(posedge i_clk)
		tx_data <= outBuffer[tail];

	// We increment the pointer to where we read from any time 1) we are
	// requesting to transmit a character, and 2) the transmitter was not
	// busy and thus accepted our request.  At that time, increment the
	// pointer, and we'll be ready for another round.
	initial	tail = 8'h00;
	always @(posedge i_clk)
		if(pwr_reset)
			tail <= 8'h00;
		else if ((tx_stb)&&(!tx_busy))
		    // ready to transmit the next byte
			tail <= tail + 8'h01;
		else if (tail == lineend) begin
			// Line buffer has been emptied
			tail <= 8'h00;
        end

	// Bypass any hardware flow control
	wire	cts_n;
	assign	cts_n = 1'b0;

    // initialise transmitter
	txuart	transmitter(i_clk, pwr_reset, i_setup, tx_break,
			tx_stb, tx_data, cts_n, o_uart_tx, tx_busy);

endmodule
