#!/bin/bash

set -e

dirPath=`dirname ${BASH_SOURCE}`
#echo $dirPath

date

time $dirPath/covmat.py

date
