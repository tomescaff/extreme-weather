#!/bin/bash
# This script uses the CDO program to create CR2MET tmax DJF files

# set input and output directories
idir1=/mnt/cirrus/cr2met_prodution/data_folder_cr2met_v2_5/CR2MET_out/txn/v2.5/v2.5_R1_day/
idir2=/mnt/cirrus/cr2met_prodution/data_folder_cr2met_ERA5T_v2_5/CR2MET_out/txn/v2.5/v2.5_R1_day/

odir_1d="/home/tcarrasco/result/data/CR2MET/tmax/sliced_1day/"
odir_3d="/home/tcarrasco/result/data/CR2MET/tmax/sliced_3day/"

mkdir -p $odir_1d
mkdir -p $odir_3d

yl="2022"
yh="2023"

c0="CR2MET_tmin_tmax_v2.5_R1_day_${yl}_11_005deg.nc"
c1="CR2MET_tmin_tmax_v2.5_R1_day_${yl}_12_005deg.nc"
c2="CR2MET_tmin_tmax_v2.5_R1_day_${yh}_01_005deg.nc"
c3="CR2MET_tmin_tmax_v2.5_R1_day_${yh}_02_005deg.nc"
c4="CR2MET_tmin_tmax_v2.5_R1_day_${yh}_03_005deg.nc"

selsta_1d="-select,startdate=${yl}-12-01T00:00:00"
selend_1d="-select,enddate=${yh}-02-28T00:00:00"

selsta_3d="-select,startdate=${yl}-12-02T00:00:00"
selend_3d="-select,enddate=${yh}-02-27T00:00:00"

oname_1d="CR2MET_tmax_v2.5_DJF_1day_${yh}_005deg.nc"
oname_3d="CR2MET_tmax_v2.5_DJF_3day_${yh}_005deg.nc"

cdo -L -O -z zip_9 -timmax $selsta_1d $selend_1d -select,name=tmax -mergetime $idir1$c0 $idir2$c1 $idir2$c2 $idir2$c3 $idir2$c4 $odir_1d$oname_1d
cdo -L -O -z zip_9 -timmax $selsta_3d $selend_3d -runmean,3 -select,name=tmax -mergetime $idir1$c0 $idir2$c1 $idir2$c2 $idir2$c3 $idir2$c4 $odir_3d$oname_3d  






