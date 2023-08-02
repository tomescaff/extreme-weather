#!/bin/bash
# This script uses the CDO program to perform the following operations
# for each file in the downloaded ACCESS HIST tas data: 
# 1) take the field mean
# 2) compute yearly values

# set input and output directories
idir="/home/tcarrasco/result/data/ACCESS/tas/orig/HIST/"
odir="/home/tcarrasco/result/data/ACCESS/tas/averaged/HIST/"

mkdir -p $odir 

fldmean="-fldmean"
yeamean="-divdpy -yearsum -muldpm"

# iterate through idir files
for file in "${idir}"*.nc
do
  echo $file # print file name
  oname=$(basename "${file%.*}-reduced.nc") # set the output file name
  opath="${odir}${oname}"
  cdo -L -O -z zip_9 $yeamean $fldmean $file $opath
done