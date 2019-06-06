// timescale does not matter any more
// it is indistinguishable in ModelSim
`timescale 1ps/1ps
module tb_top;

reg [T_IO_PAIRS*2-1:0] in, out_store;
wire [T_IO_PAIRS*2-1:0] out;

circuit dut (
.in(in),
.out(out)
);

integer i;
integer log_file;
initial
begin
  log_file = $fopen("modelsim.log", "w");
  for (i=0; i<T_ITERATIONS; i=i+1)
    begin
      in = i;
      #1;
      $fdisplay(log_file, "feedin: %d, result: %d", i, out);
    end
    $fdisplay(log_file, "Duration: %d ps", $time);
    $fclose(log_file);
    $finish;
    //$stop;
end

endmodule
