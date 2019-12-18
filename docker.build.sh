#!/bin/bash

set -e

name=s1-gcov-plant

#context=${name}
context=.

docker build ${context} \
    --no-cache \
    --file ${context}/docker/Dockerfile \
    --tag hysds/${name}:20191218
