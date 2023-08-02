#!/bin/bash
# This script uses the CDO program to ens-mean GSAT data

# set input and output directories
idir="/home/tcarrasco/result/data/ACCESS/tas/averaged/HIST/"
odir="/home/tcarrasco/result/data/ACCESS/tas/final/HIST/"

mkdir -p $odir

oname="tas_ACCESS_ensmean_spamean_yearmean_HIST.nc"

cdo -L -O -z zip_9 ensmean "${idir}*.nc" "${odir}${oname}"