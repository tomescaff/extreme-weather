#!/bin/bash
# This script uses the CDO program to: 
# 1) merge the 20060101-20801231 files with the 20810101-21001231 ones
# in the LENS1 FU reduced data

# set input and output directories
idir="/home/tcarrasco/result/data/LENS1/tmax/reduced/FU/"
odir="/home/tcarrasco/result/data/LENS1/tmax/merged/FU/"

mkdir -p $odir

# files with problems
for i in $(seq -f "%02g" 1 33)
do
    p1="${idir}b.e11.BRCP85C5CNBDRD.f09_g16.0${i}.cam.h1.TREFHTMX.20060101-20801231-reduced.nc"
    p2="${idir}b.e11.BRCP85C5CNBDRD.f09_g16.0${i}.cam.h1.TREFHTMX.20810101-21001231-reduced.nc"
    oname="b.e11.BRCP85C5CNBDRD.f09_g16.0${i}.cam.h1.TREFHTMX.20060101-21001231-merged.nc"
    cdo -L -O -z zip_9 -mergetime $p1 $p2 "${odir}${oname}"
done

# files already merged
for j in $(seq -f "%03g" 34 35; seq -f "%03g" 101 105)
do
    q1="${idir}b.e11.BRCP85C5CNBDRD.f09_g16.${j}.cam.h1.TREFHTMX.20060101-21001231-reduced.nc"
    q2="${odir}b.e11.BRCP85C5CNBDRD.f09_g16.${j}.cam.h1.TREFHTMX.20060101-21001231-merged.nc"
    ln -s $q1 $q2
done
