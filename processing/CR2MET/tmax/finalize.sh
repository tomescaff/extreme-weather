#!/bin/bash
# This script uses the CDO program to merge CR2MET tmax DJF files

# set input and output directories
idir_1d="/home/tcarrasco/result/data/CR2MET/tmax/sliced_1day/"
idir_3d="/home/tcarrasco/result/data/CR2MET/tmax/sliced_3day/"

odir="/home/tcarrasco/result/data/CR2MET/tmax/final/"

mkdir -p $odir

oname_1d="CR2MET_tmax_1day_DJF_1960_2023_chile_005deg.nc"
oname_3d="CR2MET_tmax_3day_DJF_1960_2023_chile_005deg.nc"

cdo -L -O -z zip_9 -mergetime "${idir_1d}*.nc" $odir$oname_1d
cdo -L -O -z zip_9 -mergetime "${idir_3d}*.nc" $odir$oname_3d

ncatted -a units,tmax,o,c,'degree_Celsius' $odir$oname_1d # change units' name
ncatted -a standard_name,tmax,o,c,'air_temperature' $odir$oname_1d # add std name
ncatted -a long_name,tmax,o,c,'maximum temperature over austral summer' $odir$oname_1d # change long name
ncatted -a cell_methods,tmax,o,c,'time: maximum (interval: 1 day) time: maximum (interval: 90 days comment: DJF)' $odir$oname_1d # add cell_methods
ncatted -h -a history,global,d,, $odir$oname_1d # delete history

ncatted -a units,tmax,o,c,'degree_Celsius' $odir$oname_3d # change units' name
ncatted -a standard_name,tmax,o,c,'air_temperature' $odir$oname_3d # add std name
ncatted -a long_name,tmax,o,c,'maximum 3-day temperature over austral summer' $odir$oname_3d # change long name
ncatted -a cell_methods,tmax,o,c,'time: maximum (interval: 1 day) time: maximum (interval: 90 days comment: DJF)' $odir$oname_3d # add cell_methods
ncatted -h -a history,global,d,, $odir$oname_3d # delete history
