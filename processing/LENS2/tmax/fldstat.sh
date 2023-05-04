# set input and output directories
idir=/home/tcarrasco/result/data/LENS2/tmax/remap/
odir=/home/tcarrasco/result/data/LENS2/tmax/fldstat/

mkdir -p $odir

# set input and output filenames
iname_1d=CESM2_LENS_tmax_1day_DJF_1851_2100_remap_CR2MET_005deg_100m.nc
oname_1d=CESM2_LENS_tmax_1day_DJF_1851_2100_fldmax_chile_30_40S_100m.nc

iname_3d=CESM2_LENS_tmax_3day_DJF_1851_2100_remap_CR2MET_005deg_100m.nc
oname_3d=CESM2_LENS_tmax_3day_DJF_1851_2100_fldmax_chile_30_40S_100m.nc

# iname_cr_1d=CESM1_LENS_tmax_1day_DJF_0501_2200_remap_CR2MET_005deg_cr.nc
# oname_cr_1d=CESM1_LENS_tmax_1day_DJF_0501_2200_fldmax_chile_30_40S_cr.nc

# iname_cr_3d=CESM1_LENS_tmax_3day_DJF_0501_2200_remap_CR2MET_005deg_cr.nc
# oname_cr_3d=CESM1_LENS_tmax_3day_DJF_0501_2200_fldmax_chile_30_40S_cr.nc

cdo -L -O -z zip_9 --reduce_dim -fldmax -sellonlatbox,-76,-68,-40,-30 "${idir}${iname_1d}" "${odir}${oname_1d}" 
cdo -L -O -z zip_9 --reduce_dim -fldmax -sellonlatbox,-76,-68,-40,-30 "${idir}${iname_3d}" "${odir}${oname_3d}" 
# cdo -L -O -z zip_9 --reduce_dim -fldmax -sellonlatbox,-76,-68,-40,-30 "${idir}${iname_cr_1d}" "${odir}${oname_cr_1d}" 
# cdo -L -O -z zip_9 --reduce_dim -fldmax -sellonlatbox,-76,-68,-40,-30 "${idir}${iname_cr_3d}" "${odir}${oname_cr_3d}" 
