#!/bin/bash
# This script uses the CDO program to time-merge the reduced ACCESS HIST data 

# set input and output directories
idir="/home/tcarrasco/result/data/ECEarth3/tas/averaged/HIST/"
odir="/home/tcarrasco/result/data/ECEarth3/tas/merged/HIST/"

mkdir -p $odir 

selsta="-select,startdate=1850-01-01T00:00:00"
selend="-select,enddate=2014-12-31T00:00:00"

for i in $(seq 1 25)
do
    if [ $i -eq 3 ] || [ $i -eq 8 ] || [ $i -eq 13 ]
    then
        echo "no data"
    else
        pwc="${idir}tas_Amon_EC-Earth3_historical_r${i}i1p1f1_gr_*-reduced.nc"
        oname="tas_Amon_EC-Earth3_historical_r${i}i1p1f1_gr_18500101-20141231-averaged.nc"
        cdo -L -O -z zip_9 $selsta $selend -mergetime $pwc "${odir}${oname}"
    fi
done