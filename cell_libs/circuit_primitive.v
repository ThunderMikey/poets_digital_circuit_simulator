module circuit_prim(
  input in0, in1,
  output out0, out1);
assign out1 = in0^in1;
assign out0 = ~in0;
endmodule
