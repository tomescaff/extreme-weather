#!/bin/bash
# This script uses the CDO program to merge the HIST and FU files
# HISTorical + FUture = EXtended

# set input and output directories
idirH="/home/tcarrasco/result/data/LENS1/tmax/reduced/HIST/"
idirF="/home/tcarrasco/result/data/LENS1/tmax/merged/FU/"
odir="/home/tcarrasco/result/data/LENS1/tmax/merged/EX/"

mkdir -p $odir

# create arrays with all the files inside HIST and FU dirs
arrH=("${idirH}"*)
arrF=("${idirF}"*)

# create an array with indexes
arrN1=($(seq -f "%03g" 1 35))
arrN2=($(seq -f "%03g" 101 105))
arrNT=( "${arrN1[@]}" "${arrN2[@]}")

# iterate through array using a counter
for ((i=0; i<${#arrH[@]}; i++)); do 
    oname="b.e11.BRCP85C5CNBDRD.f09_g16.${arrNT[$i]}.cam.h1.TREFHTMX.19200101-21001231-merged.nc"
    cdo -L -O -z zip_9 -mergetime "${arrH[$i]}" "${arrF[$i]}" "${odir}${oname}"  
done
