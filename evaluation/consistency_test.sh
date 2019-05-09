#!/bin/bash
# consistency test of POETS hardware execution time
# with random interval
# this script needs to be run in the same dir as POETS XML file
# this script will execute POETS XML file(s) in turns and
# iterate 10 times

# ARGS:
# $1: POETS XML file(s)

PTS_LOG=pts.log
PTS_T_LOG=/tmp/pts_run_time.log
TIME_LOG=time_log.csv

# setup procedure, to be run on defoe
source /local/ecad/setup-quartus17v0.bash

# delete previous logs
for xml in $1; do
  pushd `dirname $xml` > /dev/null
  rm $PTS_LOG $TIME_LOG
  # generate tinsel.elf
  pts-xmlc `basename $xml`
  # %e, %U, %S
  echo "run, sleep_before, app_time, real_time, user_time, system_time" > $TIME_LOG
  popd > /dev/null
done


for ((i=0;i<10;i++)); do
  for xml in $1; do
    pushd `dirname $xml` > /dev/null
    # random int between 1 and 10
    sleep_t=$(shuf -i 1-10 -n 1)
    echo "##### run $i #####" >> $PTS_LOG
    echo -n "$i, $sleep_t, " >> $TIME_LOG
    sleep $sleep_t
    /usr/bin/time -f "%e, %U, %S" -o $PTS_T_LOG pts-serve --headless 1 >> $PTS_LOG 2>&1
    # append times
    awk -F "," '/appWallClockTime/{printf $2", "}' measure.csv >> $TIME_LOG
    cat $PTS_T_LOG >> $TIME_LOG
    popd /dev/null
  done
done
