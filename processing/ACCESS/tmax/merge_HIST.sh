#!/bin/bash
# This script uses the CDO program to time-merge the reduced ACCESS HIST data 

# set input and output directories
idir="/home/tcarrasco/result/data/ACCESS/tmax/reduced/HIST/"
odir="/home/tcarrasco/result/data/ACCESS/tmax/merged/HIST/"

mkdir -p $odir 

for i in $(seq 1 40)
do
    p1="${idir}tasmax_day_ACCESS-ESM1-5_historical_r${i}i1p1f1_gn_18500101-18991231-reduced.nc"
    p2="${idir}tasmax_day_ACCESS-ESM1-5_historical_r${i}i1p1f1_gn_19000101-19491231-reduced.nc"
    p3="${idir}tasmax_day_ACCESS-ESM1-5_historical_r${i}i1p1f1_gn_19500101-19991231-reduced.nc"
    p4="${idir}tasmax_day_ACCESS-ESM1-5_historical_r${i}i1p1f1_gn_20000101-20141231-reduced.nc"
    oname="tasmax_day_ACCESS-ESM1-5_historical_r${i}i1p1f1_gn_18500101-20141231-reduced.nc"
    cdo -L -O -z zip_9 -mergetime $p1 $p2 $p3 $p4 "${odir}${oname}"
done