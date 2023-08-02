#!/bin/bash
# This script uses the CDO program to perform the following operations
# for each file in the downloaded ACCESS HIST tmax data: 
# 1) select only the variable of interest
# 2) select a lat-lon box
# 3) select period from 1850-12-01 to 2014-02-28
# 3) select months from Dec to Feb
# 4) delete 29-02

# set input and output directories
idir="/home/tcarrasco/result/data/ACCESS/tmax/orig/HIST/"
odir="/home/tcarrasco/result/data/ACCESS/tmax/reduced/HIST/"

mkdir -p $odir 

selvar="-selvar,tasmax"
selbox="-sellonlatbox,283,293.5,-56.5,-17"
selsta="-select,startdate=1850-12-01T00:00:00"
selend="-select,enddate=2014-03-01T00:00:00"
selmon="-select,month=1,2,12"
del29f="-delete,day=29,month=2"

# iterate through idir files
for file in "${idir}"*.nc
do
  echo $file # print file name
  oname=$(basename "${file%.*}-reduced.nc") # set the output file name
  opath="${odir}${oname}"
  cdo -L -O -z zip_9 $del29f $selmon $selend $selsta $selbox $selvar $file $opath
done