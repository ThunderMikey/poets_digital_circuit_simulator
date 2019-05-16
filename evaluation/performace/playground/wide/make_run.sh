#!/bin/bash

PROG=wide_prim

verilator -Wall --cc ${PROG}.v --exe sim_${PROG}.cpp

make -j -C obj_dir -f V${PROG}.mk

time ./obj_dir/V${PROG}
