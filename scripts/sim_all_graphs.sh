#!/bin/bash

GRAPH_DIR=graphs

graphs=`ls ${GRAPH_DIR}`

for g in $graphs; do
  make sim_results/${g%.*}.log
done

