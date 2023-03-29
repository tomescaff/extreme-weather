#!/bin/bash
# This script uses the CDO program to: 
# 1) compute DJF 1-day Tmax
# 2) compute DJF 3-day Tmax

# set input and output directories
idir="/home/tcarrasco/result/data/LENS1/tmax/merged/EX/"
odir="/home/tcarrasco/result/data/LENS1/tmax/computed/EX/"

mkdir -p $odir

selsta="-select,startdate=1920-12-02T00:00:00"
selend="-select,enddate=2100-03-01T00:00:00"

del1ma="-delete,day=1,month=3"
del2de="-delete,day=2,month=12"

# iterate through idir files
for j in $(seq -f "%03g" 1 35; seq -f "%03g" 101 105)
do
    iname="b.e11.BRCP85C5CNBDRD.f09_g16.${j}.cam.h1.TREFHTMX.19200101-21001231-merged.nc"
    oname_1d="LENS1.DJF.max.1d.TREFHTMX.${j}.nc"
    oname_3d="LENS1.DJF.max.3d.TREFHTMX.${j}.nc"

    # DJF 1-day Tmax
    cdo -L -O -z zip_9 -timselmax,90 $selsta $selend "${idir}${iname}" "${odir}${oname_1d}"

    # DJF 3-day Tmax
    cdo -L -O -z zip_9 -timselmax,88 $del1ma $del2de -runmean,3 $selsta $selend "${idir}${iname}" "${odir}${oname_3d}"
done 