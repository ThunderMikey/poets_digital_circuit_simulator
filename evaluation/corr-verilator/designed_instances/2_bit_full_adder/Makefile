obj_dir/Vfulladder: obj_dir/Vfulladder.cpp sim_main.cpp
	make -j -C obj_dir -f Vfulladder.mk Vfulladder

obj_dir/Vfulladder.cpp: sim_main.cpp fulladder.v
	verilator -Wall -cc fulladder.v --exe $<
