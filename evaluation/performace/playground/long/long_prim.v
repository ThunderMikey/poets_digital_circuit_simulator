// four primitives, 8 Is, 8 Os
parameter IO_PAIRS=4;
parameter DEPTH=879;
module long_prim(
  input [IO_PAIRS*2-1:0] in,
  output [IO_PAIRS*2-1:0] out
);

assign serialPrim[0].pIn = in;
assign out = serialPrim[DEPTH-1].pOut;

genvar gi, gj;
for(gi=0; gi<DEPTH; gi=gi+1) begin: serialPrim
  wire [IO_PAIRS*2-1:0] pIn;
  wire [IO_PAIRS*2-1:0] pOut;
  for(gj=0; gj<IO_PAIRS; gj=gj+1) begin: parallelPrim
    assign serialPrim[gi].pOut[gj*2+1] = serialPrim[gi].pIn[gj*2+1] ^ serialPrim[gi].pIn[gj*2];
    assign serialPrim[gi].pOut[gj*2] = ~ serialPrim[gi].pIn[gj*2];
    /*
    xor g1 (intercon[gi+1][gj*2+1], intercon[gi][gj*2], intercon[gi][gj*2+1]);
    nor g0 (intercon[gi+1][gj*2], intercon[gi][gj*2], intercon[gi][gj*2+1]);
    */
  end
end

// connect each set of parallel primitives in series
for(gi=0; gi<DEPTH-1; gi=gi+1) begin: interconn
  assign serialPrim[gi+1].pIn = serialPrim[gi].pOut;
end

endmodule
