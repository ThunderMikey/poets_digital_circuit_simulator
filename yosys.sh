#!/bin/bash
CD=`pwd`
UID=`id -u`
docker run --rm -it \
  --user $UID:$UID \
  -v $CD:/pdcs \
  -e LOCAL_USER_ID=`id -u $USER` \
  tmikey/yosys:latest \
  yosys -s yosys_scripts/standard.ys $@ 
