module divider_controlpath(
    input clk,
    input reset,
    input go,
    input [8:0] q,
    input [4:0] divisor,

    output reg loadd,
    output reg loadq0,
    output reg q0,
    output reg shift,
    output reg add_sub
);

    reg [4:0] current_state, next_state;
    reg [2:0] count;
    localparam LOAD           = 5'd0,
               LOAD_WAIT      = 3'd1,
               SHIFT_LEFT_1   = 5'd2,
               SUBTRACT_1     = 5'd3,
               SET_Q_1_1      = 5'd4,
               ADD_1          = 5'd5,
               SET_Q_0_1      = 5'd6,
               SHIFT_LEFT_2   = 5'd7,
               SUBTRACT_2     = 5'd8,
               SET_Q_1_2      = 5'd9,
               ADD_2          = 5'd10,
               SET_Q_0_2      = 5'd11,
               SHIFT_LEFT_3   = 5'd12,
               SUBTRACT_3     = 5'd13,
               SET_Q_1_3      = 5'd14,
               ADD_3          = 5'd15,
               SET_Q_0_3      = 5'd16,
               SHIFT_LEFT_4   = 5'd17,
               SUBTRACT_4     = 5'd18,
               SET_Q_1_4      = 5'd19,
               ADD_4          = 5'd20,
               SET_Q_0_4      = 5'd21;

    initial
    begin
        count = 2'b00;
    end

    always @*
    begin: state_table
        case (current_state)
            LOAD: next_state = go ? LOAD_WAIT : LOAD;
            LOAD_WAIT: next_state = go ? LOAD_WAIT : SHIFT_LEFT_1;
            SHIFT_LEFT_1: next_state = SUBTRACT_1;
            SUBTRACT_1: next_state = (divisor > q[8:4]) ? ADD_1 : SET_Q_1_1;
            SET_Q_1_1: next_state = SHIFT_LEFT_2;
            ADD_1: next_state = SET_Q_0_1;
            SET_Q_0_1: next_state = SHIFT_LEFT_2;
            SHIFT_LEFT_2: next_state = SUBTRACT_2;
            SUBTRACT_2: next_state = (divisor > q[8:4]) ? ADD_2 : SET_Q_1_2;
            SET_Q_1_2: next_state = SHIFT_LEFT_3;
            ADD_2: next_state = SET_Q_0_2;
            SET_Q_0_2: next_state = SHIFT_LEFT_3;
            SHIFT_LEFT_3: next_state = SUBTRACT_3;
            SUBTRACT_3: next_state = (divisor > q[8:4]) ? ADD_3 : SET_Q_1_3;
            SET_Q_1_3: next_state = SHIFT_LEFT_4;
            ADD_3: next_state = SET_Q_0_3;
            SET_Q_0_3: next_state = SHIFT_LEFT_4;
            SHIFT_LEFT_4: next_state = SUBTRACT_4;
            SUBTRACT_4: next_state = (divisor > q[8:4]) ? ADD_4 : SET_Q_1_4;
            SET_Q_1_4: next_state = LOAD;
            ADD_4: next_state = SET_Q_0_4;
            SET_Q_0_4: next_state = LOAD;
            default: next_state = LOAD;
        endcase
    end

    always @*
    begin: enable_signals
        loadd = 1'b0;
        loadq0 = 1'b0;
        q0 = 1'b0;
        shift = 1'b0;
        add_sub = 1'b0;

        case (current_state)
            LOAD: ;
            SHIFT_LEFT_1: shift = 1'b1;
            SUBTRACT_1: begin
                loadd = 1'b1;
                add_sub = 1'b1;
                end
            SET_Q_1_1: begin
                loadq0 = 1'b1;
                q0 = 1'b1;
                end
            ADD_1: begin
                loadd = 1'b1;
                add_sub = 1'b0;
                end
            SET_Q_0_1: begin
                loadq0 = 1'b1;
                q0 = 1'b0;
                end
            SHIFT_LEFT_2: shift = 1'b1;
            SUBTRACT_2: begin
                loadd = 1'b1;
                add_sub = 1'b1;
                end
            SET_Q_1_2: begin
                loadq0 = 1'b1;
                q0 = 1'b1;
                end
            ADD_2: begin
                loadd = 1'b1;
                add_sub = 1'b0;
                end
            SET_Q_0_2: begin
                loadq0 = 1'b1;
                q0 = 1'b0;
                end
            SHIFT_LEFT_3: shift = 1'b1;
            SUBTRACT_3: begin
                loadd = 1'b1;
                add_sub = 1'b1;
                end
            SET_Q_1_3: begin
                loadq0 = 1'b1;
                q0 = 1'b1;
                end
            ADD_3: begin
                loadd = 1'b1;
                add_sub = 1'b0;
                end
            SET_Q_0_3: begin
                loadq0 = 1'b1;
                q0 = 1'b0;
                end
            SHIFT_LEFT_4: shift = 1'b1;
            SUBTRACT_4: begin
                loadd = 1'b1;
                add_sub = 1'b1;
                end
            SET_Q_1_4: begin
                loadq0 = 1'b1;
                q0 = 1'b1;
                end
            ADD_4: begin
                loadd = 1'b1;
                add_sub = 1'b0;
                end
            SET_Q_0_4: begin
                loadq0 = 1'b1;
                q0 = 1'b0;
            end
        endcase
    end

    always @(posedge clk)
    begin
        if (reset)
        begin
            current_state <= LOAD;
        end
        else
            current_state <= next_state;
    end

endmodule
