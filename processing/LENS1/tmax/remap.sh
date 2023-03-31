#!/bin/bash

# set input and output directories
idir=/home/tcarrasco/result/data/LENS1/tmax/final/
odir=/home/tcarrasco/result/data/LENS1/tmax/remap/

# set input and output filenames
iname_1d=CESM1_LENS_tmax_1day_DJF_1921_2100_chile_1deg_40m.nc
oname_1d=CESM1_LENS_tmax_1day_DJF_1921_2100_remap_CR2MET_005deg_40m.nc

iname_3d=CESM1_LENS_tmax_3day_DJF_1921_2100_chile_1deg_40m.nc
oname_3d=CESM1_LENS_tmax_3day_DJF_1921_2100_remap_CR2MET_005deg_40m.nc

iname_cr_1d=CESM1_LENS_tmax_1day_DJF_0501_2200_chile_1deg_cr.nc
oname_cr_1d=CESM1_LENS_tmax_1day_DJF_0501_2200_remap_CR2MET_005deg_cr.nc

iname_cr_3d=CESM1_LENS_tmax_3day_DJF_0501_2200_chile_1deg_cr.nc
oname_cr_3d=CESM1_LENS_tmax_3day_DJF_0501_2200_remap_CR2MET_005deg_cr.nc

griddes=/home/tcarrasco/result/data/CR2MET/grid/griddes_CR2MET.txt
mask="/home/tcarrasco/result/data/CR2MET/mask/CR2MET_clmask_v2.5_mon_1960_2021_005deg.nc"

cdo -L -O -z zip_9 -setctomiss,0 -mul $mask -remapnn,$griddes "${idir}${iname_1d}" "${odir}${oname_1d}" 
cdo -L -O -z zip_9 -setctomiss,0 -mul $mask -remapnn,$griddes "${idir}${iname_3d}" "${odir}${oname_3d}" 
cdo -L -O -z zip_9 -setctomiss,0 -mul $mask -remapnn,$griddes "${idir}${iname_cr_1d}" "${odir}${oname_cr_1d}" 
cdo -L -O -z zip_9 -setctomiss,0 -mul $mask -remapnn,$griddes "${idir}${iname_cr_3d}" "${odir}${oname_cr_3d}" 

