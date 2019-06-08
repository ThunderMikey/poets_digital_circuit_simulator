#!/usr/bin/env bash

vsim -do compile.do

# wall clock time with 3 digits
export TIMEFORMAT='wallclock_time %3R'
time vsim -do sim.do

