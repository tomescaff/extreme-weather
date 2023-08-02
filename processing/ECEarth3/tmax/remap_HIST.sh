#!/bin/bash
# This script uses the CDO program to remap the final ACCESS HIST data to
# CR2MET grid

# set input and output directories
idir=/home/tcarrasco/result/data/ECEarth3/tmax/final/
odir=/home/tcarrasco/result/data/ECEarth3/tmax/remap/

mkdir -p $odir

# set input and output filenames
iname_1d=ECEarth3_tmax_1day_DJF_1851_2014_chile_100km_22m.nc
oname_1d=ECEarth3_tmax_1day_DJF_1851_2014_remap_CR2MET_005deg_22m.nc

griddes=/home/tcarrasco/result/data/CR2MET/grid/griddes_CR2MET.txt
mask="/home/tcarrasco/result/data/CR2MET/mask/CR2MET_clmask_v2.5_mon_1960_2021_005deg.nc"

cdo -L -O -z zip_9 -setctomiss,0 -mul $mask -remapnn,$griddes "${idir}${iname_1d}" "${odir}${oname_1d}" 

