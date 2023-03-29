#!/bin/bash
# This script uses the CDO program to: 
# 1) merge the reduced files from LENS1 CR data
# 2) delete dates before first DJF season and after last DJF season

# set input and output directories
idir="/home/tcarrasco/result/data/LENS1/tmax/reduced/CR/"
odir="/home/tcarrasco/result/data/LENS1/tmax/merged/CR/"

mkdir -p $odir

selsta="-select,startdate=0500-12-02T00:00:00"
selend="-select,enddate=2200-03-01T00:00:00"

oname="b.e11.B1850C5CN.f09_g16.005.cam.h1.TREFHTMX.05001202-22000301-merged.nc"
cdo -L -O -z zip_9 $selend $selsta -mergetime "${idir}*.nc" "${odir}${oname}"