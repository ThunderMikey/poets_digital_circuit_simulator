#!/bin/bash
# performance tests

# ARGS:
# $1: POETS XML file directory
#   needs to have individual XML file in each subsir

PTS_LOG=pts.log
PTS_T_LOG=/tmp/pts_run_time.log
TIME_LOG=`pwd`/time_log.csv
PTS_XMLS=`find $1 -type f -name *.xml`

# setup procedure, to be run on defoe
source /local/ecad/setup-quartus17v0.bash

# delete previous logs
for xml in ${PTS_XMLS}; do
  pushd `dirname $xml` > /dev/null
  rm $PTS_LOG
  # generate tinsel.elf
  pts-xmlc `basename $xml` > /dev/null
  popd > /dev/null
done

# %e, %U, %S
echo "appName, sleep_before, app_time, real_time, user_time, system_time" > $TIME_LOG

for xml in ${PTS_XMLS}; do
  # random int between 1 and 10
  sleep_t=$(shuf -i 1-10 -n 1)
  sleep $sleep_t
  echo -n "${xml%.*}, $sleep_t, " >> $TIME_LOG
  pushd `dirname $xml` > /dev/null
  /usr/bin/time -f "%e, %U, %S" -o $PTS_T_LOG pts-serve --headless 1 >> $PTS_LOG 2>&1
  # append times
  awk -F "," '/appWallClockTime/{printf $2", "}' measure.csv >> $TIME_LOG
  popd /dev/null
  cat $PTS_T_LOG >> $TIME_LOG
done
