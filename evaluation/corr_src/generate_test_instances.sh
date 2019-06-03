#!/bin/bash

TEMPLATE=./template/template.v
MAX_WIDTH=$1
MAX_DEPTH=$2

DRIVER=sim_main.cpp

for ((d=1; d<=${MAX_DEPTH}; d++)); do
  for ((w=1; w<=${MAX_WIDTH}; w++)); do
    inst=${w}x${d}
    inst_PATH=${inst}/${inst}.v
    cp -r template ${inst}
    mv ${inst}/template.v ${inst_PATH}
    sed -i "s/T_IO_PAIRS/${w}/g" ${inst_PATH}
    sed -i "s/T_DEPTH/${d}/g" ${inst_PATH}
    sed -i "s/T_PROG/${inst}/g" ${inst}/${DRIVER}
    sed -i "s/T_ITERATION/$((2 ** ($w*2)))/g" ${inst}/${DRIVER}
    sed -i "s/T_PROG/${inst}/g" ${inst}/make_run.sh
  done
done
