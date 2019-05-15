module our (clk);
  input clk;
  always @ (posedge clk)
  begin $display("Hello world"); $finish; end
endmodule
