module divider_wrapper(SW, KEY, CLOCK_50, LEDR, HEX0, HEX1, HEX2, HEX3, HEX4, HEX5);
    input [9:0] SW;
    input [3:0] KEY;
    input CLOCK_50;
    output [9:0] LEDR;
    output [6:0] HEX0, HEX1, HEX2, HEX3, HEX4, HEX5;

    wire [3:0] quotient;
    wire [4:0] remainder;

    divider div1(
        .clk(CLOCK_50),
        .reset(~KEY[0]),
        .go(~KEY[1]),
        .dividend(SW[7:4]),
        .divisor({1'b0, SW[3:0]}),
        .quotient(quotient),
        .remainder(remainder)
    );

    ssd h0(.in(SW[3:0]), .out(HEX0));
    ssd h1(.in(4'b0), .out(HEX1));
    ssd h2(.in(SW[7:4]), .out(HEX2));
    ssd h3(.in(4'b0), .out(HEX3));
    ssd h4(.in(quotient), .out(HEX4));
    ssd h5(.in(remainder[3:0]), .out(HEX5));

    assign LEDR = {6'b0, quotient};

endmodule