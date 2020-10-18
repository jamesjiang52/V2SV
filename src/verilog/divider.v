module divider(
    input clk,
    input reset,
    go,

    input [3:0] dividend,
    input [4:0] divisor,

    quotient,
    output [4:0] remainder
);

    wire loadd;
    wire loadq0;
    wire q0;
    wire shift;
    wire add_sub;

    wire [8:0] q;

    input go;
    output [3:0] quotient;

    divider_controlpath c0(
        .clk(clk),
        .reset(reset),
        .go(go),
        .q(q),
        .divisor(divisor),

        .loadd(loadd),
        .loadq0(loadq0),
        .q0(q0),
        .shift(shift),
        .add_sub(add_sub)
    );

    divider_datapath d0(
        .clk(clk),
        .reset(reset),
        .go(go),

        .dividend(dividend),
        .divisor(divisor),

        .loadd(loadd),
        .loadq0(loadq0),
        .q0(q0),
        .shift(shift),
        .add_sub(add_sub),

        .q(q)
    );

    assign quotient = q[3:0];
    assign remainder = q[8:4];

endmodule