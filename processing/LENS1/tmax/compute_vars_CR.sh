#!/bin/bash
# This script uses the CDO program to: 
# 1) compute DJF 1-day Tmax
# 2) compute DJF 3-day Tmax

# set input and output directories
idir="/home/tcarrasco/result/data/LENS1/tmax/merged/CR/"
odir="/home/tcarrasco/result/data/LENS1/tmax/computed/CR/"
tdir="/home/tcarrasco/result/data/LENS1/tmax/temp/"

mkdir -p $odir
mkdir -p $tdir

iname="b.e11.B1850C5CN.f09_g16.005.cam.h1.TREFHTMX.05001202-22000301-merged.nc"
oname_1d="LENS1.DJF.max.1d.TREFHTMX.CR.nc"
oname_3d="LENS1.DJF.max.3d.TREFHTMX.CR.nc"

tempname="b.e11.B1850C5CN.f09_g16.005.cam.h1.TREFHTMX.05001202-22000301-merged-3d.nc"

del1ma="-delete,day=1,month=3"
del2de="-delete,day=2,month=12"

# DJF 1-day Tmax
cdo -L -O -z zip_9 -timselmax,90 "${idir}${iname}" "${odir}${oname_1d}"

# DJF 3-day Tmax
cdo -L -O -z zip_9 -runmean,3 "${idir}${iname}" "${tdir}${tempname}"
cdo -L -O -z zip_9 -timselmax,88 $del1ma $del2de "${tdir}${tempname}" "${odir}${oname_3d}"