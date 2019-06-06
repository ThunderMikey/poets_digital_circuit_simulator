vlib work
vlog +initreg+1 -novopt "circuit.v" "tb.v"
vsim -lib work -novopt tb_top
run -all
