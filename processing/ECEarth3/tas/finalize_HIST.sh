#!/bin/bash
# This script uses the CDO program to ens-mean GSAT data

# set input and output directories
idir="/home/tcarrasco/result/data/ECEarth3/tas/merged/HIST/"
odir="/home/tcarrasco/result/data/ECEarth3/tas/final/HIST/"

mkdir -p $odir

oname="tas_ECEarth3_ensmean_spamean_yearmean_HIST.nc"

cdo -L -O -z zip_9 ensmean "${idir}*.nc" "${odir}${oname}"