#!/bin/bash
# This script uses the CDO program to fldmax the remapped ACCESS HIST final data 

# set input and output directories
idir=/home/tcarrasco/result/data/ACCESS/tmax/remap/
odir=/home/tcarrasco/result/data/ACCESS/tmax/fldstat/

mkdir -p $odir

# set input and output filenames
iname_1d=ACCESS_tmax_1day_DJF_1851_2014_remap_CR2MET_005deg_40m.nc
oname_1d=ACCESS_tmax_1day_DJF_1851_2014_fldmax_chile_30_40S_40m.nc

cdo -L -O -z zip_9 --reduce_dim -fldmax -sellonlatbox,-76,-68,-40,-30 "${idir}${iname_1d}" "${odir}${oname_1d}" 
