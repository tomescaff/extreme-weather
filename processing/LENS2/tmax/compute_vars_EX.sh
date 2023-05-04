#!/bin/bash
# This script uses the CDO program to: 
# 1) compute DJF 1-day Tmax
# 2) compute DJF 3-day Tmax

# set input and output directories
idir="/home/tcarrasco/result/data/LENS2/tmax/merged/EX/"
odir="/home/tcarrasco/result/data/LENS2/tmax/computed/EX/"

mkdir -p $odir

selsta="-select,startdate=1850-12-02T00:00:00"
selend="-select,enddate=2100-03-01T00:00:00"

del1ma="-delete,day=1,month=3"
del2de="-delete,day=2,month=12"

# iterate through idir files
for j in $(seq -f "%03g" 0 99)
do
    iname="b.e21.BHIST_BSSP370.f09_g17.LE2-${j}.cam.h1.TREFHTMX.18500101-21001231-merged.nc"
    oname_1d="LENS2.DJF.max.1d.TREFHTMX.${j}.nc"
    oname_3d="LENS2.DJF.max.3d.TREFHTMX.${j}.nc"

    # DJF 1-day Tmax
    cdo -L -O -z zip_9 -timselmax,90 $selsta $selend "${idir}${iname}" "${odir}${oname_1d}"

    # DJF 3-day Tmax
    cdo -L -O -z zip_9 -timselmax,88 $del1ma $del2de -runmean,3 $selsta $selend "${idir}${iname}" "${odir}${oname_3d}"
done 