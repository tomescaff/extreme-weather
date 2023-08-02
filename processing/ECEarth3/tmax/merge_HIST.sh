#!/bin/bash
# This script uses the CDO program to time-merge the reduced ACCESS HIST data 

# set input and output directories
idir="/home/tcarrasco/result/data/ECEarth3/tmax/reduced/HIST/"
odir="/home/tcarrasco/result/data/ECEarth3/tmax/merged/HIST/"

mkdir -p $odir 

for i in $(seq 1 25)
do
    if [ $i -eq 3 ] || [ $i -eq 8 ] || [ $i -eq 13 ]
    then
        echo "no data"
    else
        pwc="${idir}tasmax_day_EC-Earth3_historical_r${i}i1p1f1_gr_*-reduced.nc"
        oname="tasmax_day_EC-Earth3_historical_r${i}i1p1f1_gr_18500101-20141231-reduced.nc"
        cdo -L -O -z zip_9 -mergetime $pwc "${odir}${oname}"
    fi
done