#!/bin/bash
# This script uses the CDO program to compute DJF 1-day Tmax

# set input and output directories
idir="/home/tcarrasco/result/data/ACCESS/tmax/merged/HIST/"
odir="/home/tcarrasco/result/data/ACCESS/tmax/computed/HIST/"

mkdir -p $odir

# iterate through idir files
for j in $(seq 1 40)
do
    iname="tasmax_day_ACCESS-ESM1-5_historical_r${j}i1p1f1_gn_18500101-20141231-reduced.nc"
    oname="ACCESS.DJF.max.1d.tasmax.${j}.nc"

    # DJF 1-day Tmax
    cdo -L -O -z zip_9 -timselmax,90 "${idir}${iname}" "${odir}${oname}"
done 