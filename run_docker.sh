#!/bin/bash

docker run --rm -it \
  -v $PWD:/pdcs \
  -e LOCAL_USER_ID=`id -u $USER` \
  tmikey/graph_schema
