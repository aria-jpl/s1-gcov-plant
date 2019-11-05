#!/home/ops/tool/miniconda3/envs/plant/bin/python

#--------
# set up input and output dir

import sys

#if len(sys.argv) != 3:
#    print("Usage: %s inputDirPath outputDirPath" % sys.argv[0] , file=sys.stderr)
#    sys.exit(-1)

from util import get_input_dir_path, get_output_dir_path

#workDirPath = "/home/ops"
workDirPath = "."

#inputDirPath = '/var/data/coregistered_slcs-20190506161610-20190530161638/merged/'
inputDirPath = get_input_dir_path(workDirPath)
#output_dir = '~/hysds/work/output/'
outputDirPath = get_output_dir_path(workDirPath)

if None in [inputDirPath, outputDirPath]:
    print("Either inputDirPath or outputDirPath is None")
    sys.exit(-1)

print("input dir: ", inputDirPath)
print("output dir: ", outputDirPath)

#--------
# process

import os
import glob
import plant


#%matplotlib inline

FLAG_SINGLE_FILE = True

step_multilooking = True
step_beta_to_beta_naught = True
step_generate_rtc_factor = True
step_convert_to_gamma = True
step_display = True
step_geocode = True

# parameters
nlooks = [3, 9]  # [azimuth, range]

# input
#input_dir = '~/hysds/work/data/coregistered_slcs-20190506161610-20190530161638/merged/'
input_dir = inputDirPath

slc_file = os.path.join(input_dir, 'SLC/20190506/20190506.slc.full')

if FLAG_SINGLE_FILE:
    slc_files = [slc_file]
else:
    slc_files = [slc_file, slc_file]

incLocal = os.path.join(input_dir, 'geom_master/incLocal.rdr.full')

localInc = os.path.join(input_dir, 'geom_master/incLocal.rdr.full:1')
localPsi = os.path.join(input_dir, 'geom_master/incLocal.rdr.full:0')

lat_ml = os.path.join(input_dir, 'geom_master/lat.rdr')
lon_ml = os.path.join(input_dir, 'geom_master/lon.rdr')

# output
#output_dir = '~/hysds/work/output/'
output_dir = outputDirPath
beta_dir = os.path.join(output_dir, 'beta')
beta_naught_dir = os.path.join(output_dir, 'beta_naught')
gamma_naught_dir = os.path.join(output_dir, 'gamma_naught')
rtc_factor = os.path.join(gamma_naught_dir, 'sim_rtc.bin')
rtc_factor_ml = os.path.join(gamma_naught_dir, 'sim_rtc_ml.bin')
geo_dir = os.path.join(output_dir, 'geo_dir')

# PLAnT parameters
options = {}
options['force'] = True
# options['mute'] = True

display_options = {}
display_options['mute'] = True

# 2. Digital number to beta (generate covariance matrix if multiple files)
# single-file
if FLAG_SINGLE_FILE:
    output_beta = os.path.join(beta_dir, os.path.basename(slc_file))
    if step_multilooking:
        _ = plant.filter(slc_file, output_file=output_beta, square=True, nlooks=nlooks, **options)
    beta_files = [output_beta]
    
# covariance matrix
else:
    if step_multilooking:
        _ = plant.filter(slc_files, cov=True, output_dir=beta_dir, ext='.bin', nlooks=nlooks, debug=True, **options)
    beta_files = glob.glob(os.path.join(beta_dir, 'C*bin'))
    
print('beta files:', beta_files)

# Beta to beta-naught (absolute radiometric correction

beta_naught_abs_calibration_factor = 2.370000e+02

beta_naught_files = []
for beta_file in beta_files:
    print(f'converting {beta_file} to beta-naught')
    beta_naught_file = os.path.join(beta_naught_dir, os.path.basename(beta_file))
    beta_naught_files.append(beta_naught_file)
    if not step_beta_to_beta_naught:
        continue    
    # abs. calibration factor is squared because the data is squared: s1.s1* = s1**2
    plant.util(beta_file, beta_naught_abs_calibration_factor**2, div=True, output_file=beta_naught_file, **options)
    
print('beta-naught files:', beta_naught_files)

# Generate RTC correction factor

if step_generate_rtc_factor:
    _ = plant.radiometric_correction(output_file=rtc_factor, lia=localInc, psi=localPsi, simulate=True, **options)
    # multilooking RTC factor:
    _ = plant.filter(rtc_factor, output_file=rtc_factor_ml, nlooks=nlooks, **options)

gamma_naught_files = []
for beta_naught_file in beta_naught_files:
    print(f'converting {beta_naught_file} to gamma-naught')
    gamma_naught_file = os.path.join(gamma_naught_dir, os.path.basename(beta_naught_file))
    gamma_naught_files.append(gamma_naught_file)
    if not step_convert_to_gamma:
        continue
    plant.util(beta_naught_file, rtc_factor_ml, div=True, output_file=gamma_naught_file, **options)

geocoded_files = []
for gamma_naught_file in gamma_naught_files:
    geocoded_file = os.path.join(geo_dir, os.path.basename(gamma_naught_files[0]))
    geocoded_files.append(geocoded_file)
    if not step_geocode:
        continue
    _ = plant.geocode(gamma_naught_files[0], lat_file=lat_ml, lon_file=lon_ml, output_file=geocoded_file, **options)
