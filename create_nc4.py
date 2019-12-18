#!/home/ops/tool/miniconda3/envs/plant/bin/python

import os
import plant

from util import get_output_dir_path

workDirPath = "/home/ops"

outputDirPath = get_output_dir_path(workDirPath)
#outputDirPath = '/var/data/output'

if None in [outputDirPath]:
    print("Either outputDirPath is None")
    sys.exit(-1)

print("output dir: ", outputDirPath)

nc4FilePath = os.path.join(outputDirPath, "plant.nc4")

print("netcdf4 file path: ", nc4FilePath)


from util import Netcdf4Creator
netcdf4Creator = Netcdf4Creator(nc4FilePath)

path = os.path.join(outputDirPath, "beta_naught", "20190506.slc.full")
var = plant.read_image(path).get_image(0)
netcdf4Creator.add_2d_array("/beta_naught", "20190506.slc", var.dtype, var.shape, var)

path = os.path.join(outputDirPath, "gamma_naught", "sim_rtc_ml.bin")
var = plant.read_image(path).get_image(0)
netcdf4Creator.add_2d_array("/gamma_naught", "sim_rtc_ml", var.dtype, var.shape, var)

pth = os.path.join(outputDirPath, "geo_dir", "20190506.slc.full")
var = plant.read_image(path).get_image(0)
netcdf4Creator.add_2d_array("/geo_dir", "20190506.slc", var.dtype, var.shape, var)

netcdf4Creator.close()
