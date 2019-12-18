#!/bin/bash

set -e

name=s1-gcov-plant

docker run \
    --name $name \
    -v ~/hysds/s1-gcov/work/data:/var/data \
    --rm \
    -it \
    hysds/${name}:20191218 bash
