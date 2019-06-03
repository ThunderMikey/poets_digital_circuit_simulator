#!/bin/bash
# run `make_run.sh` in each directory

tests=`ls -d */`

for t in ${tests}; do
  pushd $t >/dev/null
  ./make_run.sh
  popd >/dev/null
done
