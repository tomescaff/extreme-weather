#!/bin/bash
# This script uses the CDO program to create CR2MET tmax DJF files

# set input and output directories
idir=/mnt/cirrus/cr2met_prodution/data_folder_cr2met_v2_5/CR2MET_out/txn/v2.5/v2.5_R1_day/
odir="/home/tcarrasco/result/data/CR2MET/nday/daily_spamax/"
mask="/home/tcarrasco/result/data/CR2MET/mask/CR2MET_clmask_v2.5_mon_1960_2021_005deg.nc"

mkdir -p $odir

# create arrays with all the files inside HIST and FU dirs
arrYl=($(seq 1959 2021))
arrYh=($(seq 1960 2022))

for ((i=0; i<${#arrYl[@]}; i++)); do
    yl="${arrYl[$i]}"
    yh="${arrYh[$i]}"

    c0="CR2MET_tmin_tmax_v2.5_R1_day_${yl}_11_005deg.nc"
    c1="CR2MET_tmin_tmax_v2.5_R1_day_${yl}_12_005deg.nc"
    c2="CR2MET_tmin_tmax_v2.5_R1_day_${yh}_01_005deg.nc"
    c3="CR2MET_tmin_tmax_v2.5_R1_day_${yh}_02_005deg.nc"
    c4="CR2MET_tmin_tmax_v2.5_R1_day_${yh}_03_005deg.nc"

    selsta="-select,startdate=${yl}-12-01T00:00:00"
    selend="-select,enddate=${yh}-02-28T00:00:00"
    selbox="-sellonlatbox,-76,-68,-40,-30"

    oname="CR2MET_tmax_v2.5_DJF_1day_${yh}_005deg.nc"

    cdo -L -O -z zip_9 --reduce_dim -fldmax $selbox -setctomiss,0 -mul $mask $selsta $selend -select,name=tmax -mergetime $idir$c0 $idir$c1 $idir$c2 $idir$c3 $idir$c4 $odir$oname
done





