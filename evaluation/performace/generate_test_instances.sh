#!/bin/bash

TEMPLATE=./template/template.v
MAX_DEPTH=1
MAX_WIDTH=16

for ((d=1; d<=${MAX_DEPTH}; d++)); do
  for ((w=1; w<=${MAX_WIDTH}; w++)); do
    inst=${w}x${d}
    inst_PATH=${inst}/${inst}.v
    mkdir ${inst}
    cp ${TEMPLATE} ${inst_PATH}
    sed -i "3s/T_IO_PAIRS/${w}/g" ${inst_PATH}
    sed -i "4s/T_DEPTH/${d}/g" ${inst_PATH}
  done
done
