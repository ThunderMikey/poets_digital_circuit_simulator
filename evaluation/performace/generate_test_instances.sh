#!/bin/bash

TEMPLATE=./template/template.v
INST_DIR=instances
BEGIN_WIDTH=$1
END_WIDTH=$2
MAX_DEPTH=$3
if [ -z $4 ]; then
  DEPTH_STEP=1
else
  DEPTH_STEP=$4
fi

mkdir -p $INST_DIR

for ((d=1; d<=${MAX_DEPTH}; d+=${DEPTH_STEP})); do
  for ((w=$BEGIN_WIDTH; w<=${END_WIDTH}; w++)); do
    inst=${w}x${d}
    inst_PATH=$INST_DIR/${inst}.v
    cp ${TEMPLATE} ${inst_PATH}
    sed -i "s/T_IO_PAIRS/${w}/g" ${inst_PATH}
    sed -i "s/T_DEPTH/${d}/g" ${inst_PATH}
  done
done
