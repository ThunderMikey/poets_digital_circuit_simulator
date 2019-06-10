#!/bin/bash
# run `make_run.sh` in each directory

TEST_DIR=$1

#tests=`ls -d */`
tests=`ls $TEST_DIR`

for t in ${tests}; do
  pushd $TEST_DIR/$t >/dev/null
  ./make_run.sh
  popd >/dev/null
done
