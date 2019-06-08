#!/usr/bin/env bash

TEMPLATE_DIR=./template-modelsim
COLLECTION_DIR=./modelsim_projs
BEGIN_WIDTH=$1
END_WIDTH=$2
MAX_DEPTH=$3
DEPTH_STEP=$4

mkdir -p ${COLLECTION_DIR}

for ((d=1; d<=${MAX_DEPTH}; d+=${DEPTH_STEP})); do
  for ((w=${BEGIN_WIDTH}; w<=${END_WIDTH}; w++)); do
    inst=${w}x${d}
    inst_dir=${COLLECTION_DIR}/${inst}
    cp -rT ${TEMPLATE_DIR} ${inst_dir}
    sed -i "s/T_IO_PAIRS/${w}/g" ${inst_dir}/circuit.v
    sed -i "s/T_DEPTH/${d}/g" ${inst_dir}/circuit.v
    sed -i "s/T_IO_PAIRS/${w}/g" ${inst_dir}/tb.v
    sed -i "s/T_ITERATIONS/$((2**($w*2)))/g" ${inst_dir}/tb.v
  done
done
