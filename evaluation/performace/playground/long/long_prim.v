// two primitives, 4 I/Os
parameter IO_PAIRS=2;
parameter DEPTH=32;
module long_prim(
  input [IO_PAIRS*2-1:0] in,
  output [IO_PAIRS*2-1:0] out
);

wire [IO_PAIRS*2-1:0] intercon [DEPTH:0];
assign intercon[0] = in;

genvar gi, gj;
for(gi=0; gi<DEPTH; gi=gi+1) begin: serialPrim
  for(gj=0; gj<IO_PAIRS; gj=gj+1) begin: parallelPrim
    assign intercon[gi+1][gj*2+1] = intercon[gi][gj*2] ^ intercon[gi][gj*2+1];
    assign intercon[gi+1][gj*2] = ~intercon[gi][gj*2];
    /*
    xor g1 (intercon[gi+1][gj*2+1], intercon[gi][gj*2], intercon[gi][gj*2+1]);
    nor g0 (intercon[gi+1][gj*2], intercon[gi][gj*2], intercon[gi][gj*2+1]);
    */
  end
end

assign out = intercon[DEPTH];

endmodule
