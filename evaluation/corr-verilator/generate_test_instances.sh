#!/bin/bash

TEMPLATE=./template/template.v
INST_DIR=instances
BEGIN_WIDTH=$1
END_WIDTH=$2
BEGIN_DEPTH=$3
END_DEPTH=$4
STEP_DEPTH=$5

DRIVER=sim_main.cpp

mkdir -p $INST_DIR

for ((d=$BEGIN_DEPTH; d<=${END_DEPTH}; d+=$STEP_DEPTH)); do
  for ((w=$BEGIN_WIDTH; w<=${END_WIDTH}; w++)); do
    inst=${w}x${d}
    inst_path=$INST_DIR/$inst
    inst_v=${inst_path}/${inst}.v
    cp -rT template $inst_path
    mv ${inst_path}/template.v ${inst_v}
    sed -i "s/T_IO_PAIRS/${w}/g" ${inst_v}
    sed -i "s/T_DEPTH/${d}/g" ${inst_v}
    sed -i "s/T_PROG/${inst}/g" $inst_path/${DRIVER}
    sed -i "s/T_ITERATION/$((2 ** ($w*2)))/g" $inst_path/${DRIVER}
    sed -i "s/T_PROG/${inst}/g" $inst_path/make_run.sh
  done
done
