#!/bin/bash
# This script uses the CDO program to: 
# 1) merge the reduced files from LENS1 CR data
# 2) delete dates before first DJF season and after last DJF season

# set input and output directories
idir="/home/tcarrasco/result/data/ERA5/u_10m_spamin/fldmin/"
odir="/home/tcarrasco/result/data/ERA5/u_10m_spamin/final/"

mkdir -p $odir

oname="ERA5_u10_6h_1979_2023_36_38S_preAndes_025deg_spamin_merged.nc"
cdo -L -O -z zip_9 -mergetime "${idir}*.nc" "${odir}${oname}"