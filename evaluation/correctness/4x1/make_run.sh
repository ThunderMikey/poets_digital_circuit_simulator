#!/bin/bash

PROG=4x1

verilator -Wall --cc ${PROG}.v --exe sim_main.cpp \
  --report-unoptflat

make -j -C obj_dir -f V${PROG}.mk

./obj_dir/V${PROG} > ${PROG}.log
