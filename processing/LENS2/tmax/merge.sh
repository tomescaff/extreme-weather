#!/bin/bash

# set input and output directories
idir="/home/tcarrasco/result/data/LENS2/tmax/reduced/HISTFU/"
odir="/home/tcarrasco/result/data/LENS2/tmax/merged/EX/"

mkdir -p $odir 

del1fu="-delete,day=1,month=1,year=2015"

n=0
prefix_hist='b.e21.BHISTcmip6.f09_g17.LE2'
prefix_fu='b.e21.BSSP370cmip6.f09_g17.LE2'

while read line; do
sufix=$(printf "%03d" $n)
oname="b.e21.BHIST_BSSP370.f09_g17.LE2-${sufix}.cam.h1.TREFHTMX.18500101-21001231-merged.nc"
cdo -L -O -z zip_9 -mergetime -mergetime "${idir}${prefix_hist}-${line}.cam.h1.TREFHTMX.*.nc" $del1fu -mergetime "${idir}${prefix_fu}-${line}.cam.h1.TREFHTMX.*.nc" "${odir}${oname}"
n=$((n+1))
done < $prefix_hist'.txt'

n=50
prefix_hist='b.e21.BHISTsmbb.f09_g17.LE2'
prefix_fu='b.e21.BSSP370smbb.f09_g17.LE2'

while read line; do
sufix=$(printf "%03d" $n)
oname="b.e21.BHIST_BSSP370.f09_g17.LE2-${sufix}.cam.h1.TREFHTMX.18500101-21001231-merged.nc"
cdo -L -O -z zip_9 -mergetime -mergetime "${idir}${prefix_hist}-${line}.cam.h1.TREFHTMX.*.nc" $del1fu -mergetime "${idir}${prefix_fu}-${line}.cam.h1.TREFHTMX.*.nc" "${odir}${oname}"
n=$((n+1))
done < $prefix_hist'.txt'