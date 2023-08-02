#!/bin/bash

# set input and output directories
idir="/home/tcarrasco/data_era5/"
odir="/home/tcarrasco/result/data/ERA5/t_vertical_profile/"

mkdir -p $odir 

selpoint="-remapnn,lon=288_lat=-36"

# 2017 01

file="t2m/ERA5_t2m_6h_2017_01_Global_025deg.nc"
echo $file
oname=$(basename "${file%.*}-fldmax.nc") # set the output file name
cdo -L -O -z zip_9 --reduce_dim $selpoint "${idir}${file}" "${odir}${oname}"

file="t_925/ERA5_t925_6h_2017_01_Global_025deg.nc"
echo $file
oname=$(basename "${file%.*}-fldmax.nc") # set the output file name
cdo -L -O -z zip_9 --reduce_dim $selpoint "${idir}${file}" "${odir}${oname}"

file="t_750/ERA5_t750_6h_2017_01_Global_025deg.nc"
echo $file
oname=$(basename "${file%.*}-fldmax.nc") # set the output file name
cdo -L -O -z zip_9 --reduce_dim $selpoint "${idir}${file}" "${odir}${oname}"

file="t_500/ERA5_t500_6h_2017_01_Global_025deg.nc"
echo $file
oname=$(basename "${file%.*}-fldmax.nc") # set the output file name
cdo -L -O -z zip_9 --reduce_dim $selpoint "${idir}${file}" "${odir}${oname}"

file="t_300/ERA5_t300_6h_2017_01_Global_025deg.nc"
echo $file
oname=$(basename "${file%.*}-fldmax.nc") # set the output file name
cdo -L -O -z zip_9 --reduce_dim $selpoint "${idir}${file}" "${odir}${oname}"

# 2017 02

file="t2m/ERA5_t2m_6h_2017_02_Global_025deg.nc"
echo $file
oname=$(basename "${file%.*}-fldmax.nc") # set the output file name
cdo -L -O -z zip_9 --reduce_dim $selpoint "${idir}${file}" "${odir}${oname}"

file="t_925/ERA5_t925_6h_2017_02_Global_025deg.nc"
echo $file
oname=$(basename "${file%.*}-fldmax.nc") # set the output file name
cdo -L -O -z zip_9 --reduce_dim $selpoint "${idir}${file}" "${odir}${oname}"

file="t_750/ERA5_t750_6h_2017_02_Global_025deg.nc"
echo $file
oname=$(basename "${file%.*}-fldmax.nc") # set the output file name
cdo -L -O -z zip_9 --reduce_dim $selpoint "${idir}${file}" "${odir}${oname}"

file="t_500/ERA5_t500_6h_2017_02_Global_025deg.nc"
echo $file
oname=$(basename "${file%.*}-fldmax.nc") # set the output file name
cdo -L -O -z zip_9 --reduce_dim $selpoint "${idir}${file}" "${odir}${oname}"

file="t_300/ERA5_t300_6h_2017_02_Global_025deg.nc"
echo $file
oname=$(basename "${file%.*}-fldmax.nc") # set the output file name
cdo -L -O -z zip_9 --reduce_dim $selpoint "${idir}${file}" "${odir}${oname}"

# 2023 01

file="t2m/ERA5_t2m_6h_2023_01_Global_025deg.nc"
echo $file
oname=$(basename "${file%.*}-fldmax.nc") # set the output file name
cdo -L -O -z zip_9 --reduce_dim $selpoint "${idir}${file}" "${odir}${oname}"

file="t_925/ERA5_t925_6h_2023_01_Global_025deg.nc"
echo $file
oname=$(basename "${file%.*}-fldmax.nc") # set the output file name
cdo -L -O -z zip_9 --reduce_dim $selpoint "${idir}${file}" "${odir}${oname}"

file="t_750/ERA5_t750_6h_2023_01_Global_025deg.nc"
echo $file
oname=$(basename "${file%.*}-fldmax.nc") # set the output file name
cdo -L -O -z zip_9 --reduce_dim $selpoint "${idir}${file}" "${odir}${oname}"

file="t_500/ERA5_t500_6h_2023_01_Global_025deg.nc"
echo $file
oname=$(basename "${file%.*}-fldmax.nc") # set the output file name
cdo -L -O -z zip_9 --reduce_dim $selpoint "${idir}${file}" "${odir}${oname}"

file="t_300/ERA5_t300_6h_2023_01_Global_025deg.nc"
echo $file
oname=$(basename "${file%.*}-fldmax.nc") # set the output file name
cdo -L -O -z zip_9 --reduce_dim $selpoint "${idir}${file}" "${odir}${oname}"

# 2017 02

file="t2m/ERA5_t2m_6h_2023_02_Global_025deg.nc"
echo $file
oname=$(basename "${file%.*}-fldmax.nc") # set the output file name
cdo -L -O -z zip_9 --reduce_dim $selpoint "${idir}${file}" "${odir}${oname}"

file="t_925/ERA5_t925_6h_2023_02_Global_025deg.nc"
echo $file
oname=$(basename "${file%.*}-fldmax.nc") # set the output file name
cdo -L -O -z zip_9 --reduce_dim $selpoint "${idir}${file}" "${odir}${oname}"

file="t_750/ERA5_t750_6h_2023_02_Global_025deg.nc"
echo $file
oname=$(basename "${file%.*}-fldmax.nc") # set the output file name
cdo -L -O -z zip_9 --reduce_dim $selpoint "${idir}${file}" "${odir}${oname}"

file="t_500/ERA5_t500_6h_2023_02_Global_025deg.nc"
echo $file
oname=$(basename "${file%.*}-fldmax.nc") # set the output file name
cdo -L -O -z zip_9 --reduce_dim $selpoint "${idir}${file}" "${odir}${oname}"

file="t_300/ERA5_t300_6h_2023_02_Global_025deg.nc"
echo $file
oname=$(basename "${file%.*}-fldmax.nc") # set the output file name
cdo -L -O -z zip_9 --reduce_dim $selpoint "${idir}${file}" "${odir}${oname}"