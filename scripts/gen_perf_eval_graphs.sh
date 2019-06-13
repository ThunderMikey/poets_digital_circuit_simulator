#!/bin/bash

VERILOG_HOME=evaluation/performace
YOSYS_TEMPLATE=yosys_scripts/perf_template.ys
BEGIN_WIDTH=$1
END_WIDTH=$2
BEGIN_DEPTH=$3
END_DEPTH=$4
DEPTH_STEP=$5

# generate Verilogs
pushd ${VERILOG_HOME}
./generate_test_instances.sh $BEGIN_WIDTH ${END_WIDTH} ${BEGIN_DEPTH} ${END_DEPTH} ${DEPTH_STEP}
popd

# generate yosys scripts
for ((d=$BEGIN_DEPTH; d<=${END_DEPTH}; d+=${DEPTH_STEP})); do
  for ((w=$BEGIN_WIDTH; w<=${END_WIDTH}; w++)); do
    inst=${w}x${d}
    inst_PATH=yosys_scripts/${inst}.ys
    cp ${YOSYS_TEMPLATE} ${inst_PATH}
    sed -i "s:T_VERILOG_PATH:evaluation/performace/instances/${inst}.v:g" ${inst_PATH}
    sed -i "s:T_EDIF_PATH:netlists/${inst}.edif:g" ${inst_PATH}
  done
done

# call make commands
for ((d=$BEGIN_DEPTH; d<=${END_DEPTH}; d+=${DEPTH_STEP})); do
  for ((w=$BEGIN_WIDTH; w<=${END_WIDTH}; w++)); do
    inst=${w}x${d}
    make graphs/${inst}.xml
  done
done
