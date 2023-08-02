#!/bin/bash
# This script uses the CDO program to compute DJF 1-day Tmax

# set input and output directories
idir="/home/tcarrasco/result/data/ECEarth3/tmax/merged/HIST/"
odir="/home/tcarrasco/result/data/ECEarth3/tmax/computed/HIST/"

mkdir -p $odir

for i in $(seq 1 25)
do
    if [ $i -eq 3 ] || [ $i -eq 8 ] || [ $i -eq 13 ]
    then
        echo "no data"
    else
        iname="tasmax_day_EC-Earth3_historical_r${i}i1p1f1_gr_18500101-20141231-reduced.nc"
        oname="ECEarth3.DJF.max.1d.tasmax.${i}.nc"
        # DJF 1-day Tmax
        cdo -L -O -z zip_9 -timselmax,90 "${idir}${iname}" "${odir}${oname}"
    fi
done