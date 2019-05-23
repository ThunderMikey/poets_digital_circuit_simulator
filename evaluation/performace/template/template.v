// this is a template
// T_IO_PAIRS, T_DEPTH need to be replaced by numbers
parameter IO_PAIRS=T_IO_PAIRS;
parameter DEPTH=T_DEPTH;
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
  end
end

// connect each set of parallel primitives in series
for(gi=0; gi<DEPTH-1; gi=gi+1) begin: interconn
  assign serialPrim[gi+1].pIn = serialPrim[gi].pOut;
end

endmodule
