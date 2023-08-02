#!/bin/bash

# set input and output directories
idir="/home/tcarrasco/data_era5/v_10m/"
odir="/home/tcarrasco/result/data/ERA5/v_10m_spamax/fldmax/"

mkdir -p $odir 

selbox="-sellonlatbox,285.5,286.5,-38,-36"

# iterate through idir files
for file in "${idir}"*.nc
do
  echo $file # print file name
  oname=$(basename "${file%.*}-fldmax.nc") # set the output file name
  opath="${odir}${oname}"
  cdo -L -O -z zip_9 --reduce_dim -fldmax $selbox $file $opath
done