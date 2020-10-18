module divider_datapath(
    input clk,
    input reset,
    input go,
    input [3:0] dividend,
    input [4:0] divisor,

    input loadd,
    input loadq0,
    input q0,
    input shift,
    input add_sub,

    output reg [8:0] q
);

    reg [4:0] sum;

    always @*
        sum = add_sub ? q[8:4] - divisor : q[8:4] + divisor;

    always @(posedge clk)
    begin
        if (reset)
            q <= 9'b0;
        else if (go)
            q <= {5'b0, dividend};
        else if (loadq0)
            q[0] <= q0;
        else if (loadd)
            q[8:4] <= sum;
        else if (shift)
        begin
            q[8] <= q[7];
            q[7] <= q[6];
            q[6] <= q[5];
            q[5] <= q[4];
            q[4] <= q[3];
            q[3] <= q[2];
            q[2] <= q[1];
            q[1] <= q[0];
            q[0] <= 1'b0;
        end
    end

endmodule