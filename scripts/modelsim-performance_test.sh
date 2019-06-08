#!/bin/bash
# performance tests

# ARGS:
# $1: ModelSim projects dir
#   needs to have individual do, Verilog, run_sim.sh in each subsir

PTS_T_LOG=/tmp/pts_run_time.log
TIME_LOG=`pwd`/time_log.csv
MS_PROJ_DIR=$1
MS_PROJS=`ls $1`


# %e, %U, %S
echo "width, depth, real_time" > $TIME_LOG

for pj in ${MS_PROJS}; do
  app_name=`basename ${pj}`
  width=`echo $app_name | cut -d'x' -f 1`
  depth=`echo $app_name | cut -d'x' -f 2`
  proj_dir=$MS_PROJ_DIR/$pj
  echo $proj_dir

  echo -n "$width, $depth, " >> $TIME_LOG
  pushd $proj_dir > /dev/null
  wall_time=`./run_sim.sh 2>&1 | awk '/wallclock_time/{print $2}'`
  echo "$wall_time" >> $TIME_LOG
  popd > /dev/null
done
