#!/bin/bash

set -e

dirPath=`dirname ${BASH_SOURCE}`
#echo $dirPath

date

time $dirPath/covmat.py

time $dirPath/create_nc4.py

date
