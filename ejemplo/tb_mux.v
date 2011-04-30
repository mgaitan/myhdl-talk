module tb_mux;

reg [0:0] s;
wire [31:0] o;
reg [31:0] a;
reg [31:0] b;

initial begin
    $from_myhdl(
        s,
        a,
        b
    );
    $to_myhdl(
        o
    );
end

mux dut(
    s,
    o,
    a,
    b
);

endmodule
