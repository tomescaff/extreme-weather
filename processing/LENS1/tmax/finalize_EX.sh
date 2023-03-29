#!/bin/bash

# set input and output directories
idir=/home/tcarrasco/result/data/LENS1/tmax/computed/EX/
odir=/home/tcarrasco/result/data/LENS1/tmax/final/

# set input and output filenames
iname_1d=LENS1.DJF.max.1d.TREFHTMX.*.nc
oname_1d=temp_1d.nc
oname_1d_degc=CESM1_LENS_tmax_1day_DJF_1921_2100_chile_1deg_40m.nc

iname_3d=LENS1.DJF.max.3d.TREFHTMX.*.nc
oname_3d=temp_3d.nc
oname_3d_degc=CESM1_LENS_tmax_3day_DJF_1921_2100_chile_1deg_40m.nc

# operations over 1d netcdf file
ncecat $idir$iname_1d -O $odir$oname_1d # create ensemble
ncpdq -a time,record $odir$oname_1d -O $odir$oname_1d # swap dimensions
ncrename -h -O -d record,ensemble $odir$oname_1d # change name of var
ncrename -h -O -v TREFHTMX,tmax $odir$oname_1d # change name of var
ncatted -a units,tmax,o,c,'degree_Celsius' $odir$oname_1d # change units' name
ncatted -a standard_name,tmax,o,c,'air_temperature' $odir$oname_1d # add std name
ncatted -a long_name,tmax,o,c,'maximum temperature over austral summer' $odir$oname_1d # change long name
ncatted -a cell_methods,tmax,o,c,'time: maximum (interval: 1 day) time: maximum (interval: 90 days comment: DJF)' $odir$oname_1d # add cell_methods
cdo -L -O -z zip_9  -addc,-273.15 $odir$oname_1d $odir$oname_1d_degc # from K to C
ncatted -h -a history,global,d,, $odir$oname_1d_degc # delete history

# operations over 3d netcdf file
ncecat $idir$iname_3d -O $odir$oname_3d # create ensemble
ncpdq -a time,record $odir$oname_3d -O $odir$oname_3d # swap dimensions
ncrename -h -O -d record,ensemble $odir$oname_3d # change name of var
ncrename -h -O -v TREFHTMX,tmax $odir$oname_3d # change name of var
ncatted -a units,tmax,o,c,'degree_Celsius' $odir$oname_3d # change units' name
ncatted -a standard_name,tmax,o,c,'air_temperature' $odir$oname_3d # add std name
ncatted -a long_name,tmax,o,c,'maximum 3-day temperature over austral summer' $odir$oname_3d # change long name
ncatted -a cell_methods,tmax,o,c,'time: maximum (interval: 1 day) time: mean (interval: 3 days comment: rolling mean) time: maximum (interval: 90 days comment: DJF)' $odir$oname_3d # add cell_methods
cdo -L -O -z zip_9  -addc,-273.15 $odir$oname_3d $odir$oname_3d_degc # from K to C
ncatted -h -a history,global,d,, $odir$oname_3d_degc # delete history

# remove temporary files
rm $odir$oname_1d
rm $odir$oname_3d
