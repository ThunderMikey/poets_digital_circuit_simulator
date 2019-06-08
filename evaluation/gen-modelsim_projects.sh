#!/usr/bin/env bash

TEMPLATE_DIR=./template-modelsim
COLLECTION_DIR=./modelsim_projs
MAX_WIDTH=$1
MAX_DEPTH=$2
DEPTH_STEP=$3

mkdir -p ${COLLECTION_DIR}

for ((d=1; d<=${MAX_DEPTH}; d+=${DEPTH_STEP})); do
  for ((w=1; w<=${MAX_WIDTH}; w++)); do
    inst=${w}x${d}
    inst_dir=${COLLECTION_DIR}/${inst}
    cp -rT ${TEMPLATE_DIR} ${inst_dir}
    sed -i "s/T_IO_PAIRS/${w}/g" ${inst_dir}/circuit.v
    sed -i "s/T_DEPTH/${d}/g" ${inst_dir}/circuit.v
    sed -i "s/T_IO_PAIRS/${w}/g" ${inst_dir}/tb.v
    sed -i "s/T_ITERATIONS/$((2**($w*2)))/g" ${inst_dir}/tb.v
  done
done
