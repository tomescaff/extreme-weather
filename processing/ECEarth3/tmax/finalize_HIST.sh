#!/bin/bash

# set input and output directories
idir=/home/tcarrasco/result/data/ECEarth3/tmax/computed/HIST/
odir=/home/tcarrasco/result/data/ECEarth3/tmax/final/

mkdir -p $odir

# set input and output filenames
iname_1d=ECEarth3.DJF.max.1d.tasmax.*.nc
oname_1d=temp_1d.nc
oname_1d_degc=ECEarth3_tmax_1day_DJF_1851_2014_chile_100km_22m.nc

# operations over 1d netcdf file
ncecat $idir$iname_1d -O $odir$oname_1d # create ensemble
ncatted -O -a coordinates,tasmax,d,, $odir$oname_1d # delete coordinates 
ncpdq -a time,record $odir$oname_1d -O $odir$oname_1d # swap dimensions
ncrename -h -O -d record,ensemble $odir$oname_1d # change name of var
ncrename -h -O -v tasmax,tmax $odir$oname_1d # change name of var
ncatted -a units,tmax,o,c,'degree_Celsius' $odir$oname_1d # change units' name
ncatted -a standard_name,tmax,o,c,'air_temperature' $odir$oname_1d # add std name
ncatted -a long_name,tmax,o,c,'maximum temperature over austral summer' $odir$oname_1d # change long name
ncatted -a cell_methods,tmax,o,c,'time: maximum (interval: 1 day) time: maximum (interval: 90 days comment: DJF)' $odir$oname_1d # add cell_methods
cdo -L -O -z zip_9  -addc,-273.15 $odir$oname_1d $odir$oname_1d_degc # from K to C
ncatted -h -a history,global,d,, $odir$oname_1d_degc # delete history

# remove temporary files
rm $odir$oname_1d
