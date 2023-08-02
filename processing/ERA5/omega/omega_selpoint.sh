#!/bin/bash

# set input and output directories
idir="/home/tcarrasco/data_era5/w_500/"
odir="/home/tcarrasco/result/data/ERA5/w500_preandes/"

mkdir -p $odir 

selpoint="-remapnn,lon=-71.25_lat=-36" # preandes
# selpoint="-remapnn,lon=-72_lat=-36" # valley
# selpoint="-remapnn,lon=-73.5_lat=-36" # coast

# iterate through idir files
for file in "${idir}"*.nc
do
  echo $file # print file name
  oname=$(basename "${file%.*}-selpoint.nc") # set the output file name
  opath="${odir}${oname}"
  cdo -L -O -z zip_9 --reduce_dim $selpoint $file $opath
done