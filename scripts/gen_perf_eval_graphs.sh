#!/bin/bash

VERILOG_HOME=evaluation/performace
YOSYS_TEMPLATE=yosys_scripts/perf_template.ys
MAX_WIDTH=16
MAX_DEPTH=1

# generate Verilogs
pushd ${VERILOG_HOME}
./generate_test_instances.sh ${MAX_WIDTH} ${MAX_DEPTH}
popd

# generate yosys scripts
for ((d=1; d<=${MAX_DEPTH}; d++)); do
  for ((w=1; w<=${MAX_WIDTH}; w++)); do
    inst=${w}x${d}
    inst_PATH=yosys_scripts/${inst}.ys
    cp ${YOSYS_TEMPLATE} ${inst_PATH}
    sed -i "s:T_VERILOG_PATH:evaluation/performace/${inst}/${inst}.v:g" ${inst_PATH}
    sed -i "s:T_EDIF_PATH:netlists/${inst}.edif:g" ${inst_PATH}
  done
done

# call make commands
for ((d=1; d<=${MAX_DEPTH}; d++)); do
  for ((w=1; w<=${MAX_WIDTH}; w++)); do
    inst=${w}x${d}
    make graphs/${inst}.xml
  done
done
