#!/bin/bash
# This script uses the CDO program to: 
# 1) merge the reduced files from LENS1 CR data
# 2) delete dates before first DJF season and after last DJF season

# set input and output directories
idir="/home/tcarrasco/result/data/ERA5/w500_preandes/selpoint/"
odir="/home/tcarrasco/result/data/ERA5/w500_preandes/final/"

mkdir -p $odir

oname="ERA5_w500_6h_1979_2023_preandes_025deg_selpoint_merged.nc"
cdo -L -O -z zip_9 -mergetime "${idir}*.nc" "${odir}${oname}"