#!/bin/bash

set -e

eval "$($HOME/tool/miniconda3/bin/conda shell.bash hook)"

conda create --name plant
conda activate plant
conda install -c plant plant

conda install -c plant netCDF4
