#!/bin/bash

# set input and output directories
idir="/home/tcarrasco/data_era5/u_10m/"
odir="/home/tcarrasco/result/data/ERA5/u_10m_spamin/fldmin/"

mkdir -p $odir 

selbox="-sellonlatbox,287.5,288.5,-38,-36"

# iterate through idir files
for file in "${idir}"*.nc
do
  echo $file # print file name
  oname=$(basename "${file%.*}-fldmin.nc") # set the output file name
  opath="${odir}${oname}"
  cdo -L -O -z zip_9 --reduce_dim -fldmin $selbox $file $opath
done