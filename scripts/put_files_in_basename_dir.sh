#!/bin/bash

working=$1
FILES=`ls ${working}`

for f in ${FILES}; do
  newDir=${working}/${f%.*}
  mkdir ${newDir}
  mv ${working}/$f ${newDir}/
done
