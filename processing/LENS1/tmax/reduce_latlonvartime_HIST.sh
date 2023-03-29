#!/bin/bash
# This script uses the CDO program to select: 
# 1) only the variable of interest
# 2) a lat-lon box
# 3) time between 1920-01-01 and 2005-12-31
# 4) months from Dec to March
# 5) delete from 03-02 to 03-31
# 6) delete 12-01
# from each file of the downloaded LENS1 HIST data

# set input and output directories
idir="/home/tcarrasco/result/data/LENS1/tmax/orig/HIST/"
odir="/home/tcarrasco/result/data/LENS1/tmax/reduced/HIST/"

mkdir -p $odir 

seqnum="$(seq -s, 2 31)"
del1de="-delete,day=1,month=12"
delmar="-delete,day=${seqnum},month=3"
selmon="-select,month=1,2,3,12"
selsta="-select,startdate=1920-01-01T00:00:00"
selbox="-sellonlatbox,283,293.5,-56.5,-17"
selvar="-selvar,TREFHTMX"

# iterate through idir files
for file in "${idir}"*
do
  echo $file # print file name
  oname=$(basename "${file%.*}-reduced.nc") # set the output file name
  opath="${odir}${oname}"
  cdo -L -O -z zip_9 $del1de $delmar $selmon $selsta $selbox $selvar $file $opath
done