#!/bin/bash

TEMPLATE=./template/template.v
MAX_WIDTH=$1
MAX_DEPTH=$2
if [ -z $3 ]; then
  DEPTH_STEP=1
else
  DEPTH_STEP=$3
fi

for ((d=1; d<=${MAX_DEPTH}; d+=${DEPTH_STEP})); do
  for ((w=1; w<=${MAX_WIDTH}; w++)); do
    inst=${w}x${d}
    inst_PATH=${inst}/${inst}.v
    mkdir ${inst}
    cp ${TEMPLATE} ${inst_PATH}
    sed -i "s/T_IO_PAIRS/${w}/g" ${inst_PATH}
    sed -i "s/T_DEPTH/${d}/g" ${inst_PATH}
  done
done
