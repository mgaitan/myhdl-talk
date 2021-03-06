// File: mux.v
// Generated by MyHDL 0.6
// Date: Sat Apr 30 03:27:01 2011

`timescale 1ns/10ps

module mux (
    s,
    o,
    a,
    b
);

input [0:0] s;
output [31:0] o;
reg [31:0] o;
input [31:0] a;
input [31:0] b;




always @(a, s, b) begin: MUX_LOGIC
    if ((s == 0)) begin
        o <= a;
    end
    else begin
        o <= b;
    end
end

endmodule
