parameter SIZE=32;
module wide_prim(
  input [SIZE*2-1:0] in,
  output [SIZE*2-1:0] out
);

genvar gi;

for(gi=0; gi<SIZE; gi=gi+1) begin: primLadder
  assign out[gi*2+1] = in[gi*2] ^ in[gi*2+1];
  assign out[gi*2] = ~(in[gi*2] | in[gi*2+1]);
end

endmodule
