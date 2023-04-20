#!/bin/bash
# This script uses the CDO program to: 
# 1) compute fldmean tas
# 2) merge files
# 3) compute 12 month resample

# set input and output directories
idir="/home/tcarrasco/result/data/LENS1/tas/orig/CR/"
odir="/home/tcarrasco/result/data/LENS1/tas/reduced/CR/"
fdir="/home/tcarrasco/result/data/LENS1/tas/final/"
mkdir -p $odir
mkdir -p $fdir

# iterate through idir files
for file in "${idir}"*
do
  echo $file # print file name
  oname=$(basename "${file%.*}-fldmean.nc") # set the output file name
  opath="${odir}${oname}"
  cdo -L -O -z zip_9 --reduce_dim -fldmean -selvar,TREFHT $file $opath
done

cdo -L -O -z zip_9 -timselmean,12 -mergetime "${odir}*-fldmean.nc" "${fdir}CESM1_LENS_tas_annual_0400_2200_global_mean_cr.nc"

