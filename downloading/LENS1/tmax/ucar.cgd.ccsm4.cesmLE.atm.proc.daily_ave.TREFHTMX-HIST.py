#!/usr/bin/env python3

import hashlib
import urllib.request
import shutil
import os
from urllib.parse import urlparse
import sys
from platform import python_version

PYTHON_VERSION=python_version()
# if PYTHON_VERSION is None:
#     PYTHON_VERSION=PARSE_ERROR

PYTHON_USER_AGENT="python/" + PYTHON_VERSION + "/esg/4.3.1-20230321-173145/created/2023-03-25T14:28:38-06:00"

################################################################
#
# Climate Data Gateway download script
#
#
# Generated by: NCAR Climate Data Gateway
#
# Your download selection includes data that might be secured using API Token based
# authentication. Therefore, this script can have your api-token. If you
# re-generate your API Token after you download this script, the download will
# fail. If that happens, you can either re-download this script or you can replace
# the old API Token with the new one by going to the Account Home:
#
# https://www.earthsystemgrid.org/account/user/account-home.html
#
# and clicking on "API Token" link under "Personal Account". You will be asked
# to log into the application before you can view your API Token.
#
# Usage: python3 python-ucar.cgd.ccsm4.cesmLE.atm.proc.daily_ave.TREFHTMX-20230325T1428Z.py
# Version: 0.1.0-alpha
#
#
# Dataset
# ucar.cgd.ccsm4.cesmLE.atm.proc.daily_ave.TREFHTMX
# ec499922-cfc9-42c7-a860-e3d9610bb0b8
# https://www.earthsystemgrid.org/dataset/ucar.cgd.ccsm4.cesmLE.atm.proc.daily_ave.TREFHTMX.html
# https://www.earthsystemgrid.org/dataset/id/ec499922-cfc9-42c7-a860-e3d9610bb0b8.html
#
# Dataset Version
# 4
# c9292fb4-b515-4129-8dee-97b4f8aeba8b
# https://www.earthsystemgrid.org/dataset/ucar.cgd.ccsm4.cesmLE.atm.proc.daily_ave.TREFHTMX/version/4.html
# https://www.earthsystemgrid.org/dataset/version/id/c9292fb4-b515-4129-8dee-97b4f8aeba8b.html
#
################################################################

print("This Python 3 download script is experimental.  Please provide feedback at 'esg-support@earthsystemgrid.org'.")
print("")

urls = [
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/daily/TREFHTMX/b.e11.B20TRC5CNBDRD.f09_g16.001.cam.h1.TREFHTMX.18500101-20051231.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/daily/TREFHTMX/b.e11.B20TRC5CNBDRD.f09_g16.002.cam.h1.TREFHTMX.19200101-20051231.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/daily/TREFHTMX/b.e11.B20TRC5CNBDRD.f09_g16.003.cam.h1.TREFHTMX.19200101-20051231.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/daily/TREFHTMX/b.e11.B20TRC5CNBDRD.f09_g16.004.cam.h1.TREFHTMX.19200101-20051231.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/daily/TREFHTMX/b.e11.B20TRC5CNBDRD.f09_g16.005.cam.h1.TREFHTMX.19200101-20051231.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/daily/TREFHTMX/b.e11.B20TRC5CNBDRD.f09_g16.006.cam.h1.TREFHTMX.19200101-20051231.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/daily/TREFHTMX/b.e11.B20TRC5CNBDRD.f09_g16.007.cam.h1.TREFHTMX.19200101-20051231.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/daily/TREFHTMX/b.e11.B20TRC5CNBDRD.f09_g16.008.cam.h1.TREFHTMX.19200101-20051231.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/daily/TREFHTMX/b.e11.B20TRC5CNBDRD.f09_g16.009.cam.h1.TREFHTMX.19200101-20051231.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/daily/TREFHTMX/b.e11.B20TRC5CNBDRD.f09_g16.010.cam.h1.TREFHTMX.19200101-20051231.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/daily/TREFHTMX/b.e11.B20TRC5CNBDRD.f09_g16.011.cam.h1.TREFHTMX.19200101-20051231.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/daily/TREFHTMX/b.e11.B20TRC5CNBDRD.f09_g16.012.cam.h1.TREFHTMX.19200101-20051231.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/daily/TREFHTMX/b.e11.B20TRC5CNBDRD.f09_g16.013.cam.h1.TREFHTMX.19200101-20051231.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/daily/TREFHTMX/b.e11.B20TRC5CNBDRD.f09_g16.014.cam.h1.TREFHTMX.19200101-20051231.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/daily/TREFHTMX/b.e11.B20TRC5CNBDRD.f09_g16.015.cam.h1.TREFHTMX.19200101-20051231.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/daily/TREFHTMX/b.e11.B20TRC5CNBDRD.f09_g16.016.cam.h1.TREFHTMX.19200101-20051231.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/daily/TREFHTMX/b.e11.B20TRC5CNBDRD.f09_g16.017.cam.h1.TREFHTMX.19200101-20051231.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/daily/TREFHTMX/b.e11.B20TRC5CNBDRD.f09_g16.018.cam.h1.TREFHTMX.19200101-20051231.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/daily/TREFHTMX/b.e11.B20TRC5CNBDRD.f09_g16.019.cam.h1.TREFHTMX.19200101-20051231.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/daily/TREFHTMX/b.e11.B20TRC5CNBDRD.f09_g16.020.cam.h1.TREFHTMX.19200101-20051231.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/daily/TREFHTMX/b.e11.B20TRC5CNBDRD.f09_g16.021.cam.h1.TREFHTMX.19200101-20051231.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/daily/TREFHTMX/b.e11.B20TRC5CNBDRD.f09_g16.022.cam.h1.TREFHTMX.19200101-20051231.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/daily/TREFHTMX/b.e11.B20TRC5CNBDRD.f09_g16.023.cam.h1.TREFHTMX.19200101-20051231.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/daily/TREFHTMX/b.e11.B20TRC5CNBDRD.f09_g16.024.cam.h1.TREFHTMX.19200101-20051231.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/daily/TREFHTMX/b.e11.B20TRC5CNBDRD.f09_g16.025.cam.h1.TREFHTMX.19200101-20051231.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/daily/TREFHTMX/b.e11.B20TRC5CNBDRD.f09_g16.026.cam.h1.TREFHTMX.19200101-20051231.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/daily/TREFHTMX/b.e11.B20TRC5CNBDRD.f09_g16.027.cam.h1.TREFHTMX.19200101-20051231.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/daily/TREFHTMX/b.e11.B20TRC5CNBDRD.f09_g16.028.cam.h1.TREFHTMX.19200101-20051231.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/daily/TREFHTMX/b.e11.B20TRC5CNBDRD.f09_g16.029.cam.h1.TREFHTMX.19200101-20051231.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/daily/TREFHTMX/b.e11.B20TRC5CNBDRD.f09_g16.030.cam.h1.TREFHTMX.19200101-20051231.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/daily/TREFHTMX/b.e11.B20TRC5CNBDRD.f09_g16.031.cam.h1.TREFHTMX.19200101-20051231.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/daily/TREFHTMX/b.e11.B20TRC5CNBDRD.f09_g16.032.cam.h1.TREFHTMX.19200101-20051231.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/daily/TREFHTMX/b.e11.B20TRC5CNBDRD.f09_g16.033.cam.h1.TREFHTMX.19200101-20051231.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/daily/TREFHTMX/b.e11.B20TRC5CNBDRD.f09_g16.034.cam.h1.TREFHTMX.19200101-20051231.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/daily/TREFHTMX/b.e11.B20TRC5CNBDRD.f09_g16.035.cam.h1.TREFHTMX.19200101-20051231.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/daily/TREFHTMX/b.e11.B20TRC5CNBDRD.f09_g16.101.cam.h1.TREFHTMX.19200101-20051231.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/daily/TREFHTMX/b.e11.B20TRC5CNBDRD.f09_g16.102.cam.h1.TREFHTMX.19200101-20051231.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/daily/TREFHTMX/b.e11.B20TRC5CNBDRD.f09_g16.103.cam.h1.TREFHTMX.19200101-20051231.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/daily/TREFHTMX/b.e11.B20TRC5CNBDRD.f09_g16.104.cam.h1.TREFHTMX.19200101-20051231.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/daily/TREFHTMX/b.e11.B20TRC5CNBDRD.f09_g16.105.cam.h1.TREFHTMX.19200101-20051231.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF']

# Gets filename even when there are parameters (but uses urlparse and os)
def get_filename(url):
    a = urlparse(url)
    return os.path.basename(a.path)

opener = urllib.request.build_opener()
opener.addheaders = [("User-agent", PYTHON_USER_AGENT)]
opener.addheaders.append(("Authorization", "api-token {}".format("Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF")))

for url in urls:
    file_name = get_filename(url)

    print("Downloading File: ", url)

    try:
        file_name = os.path.join('/home/tcarrasco/result/data/LENS1/tmax/orig/HIST/', file_name)
        with opener.open(url) as response, open(file_name, 'ab') as out_file:
            shutil.copyfileobj(response, out_file)

    except urllib.error.HTTPError as e:
    # Return code error (e.g. 404, 501, ...)
        print("HTTPError: {}".format(e.code))
    except urllib.error.URLError as e:
    # Not an HTTP-specific error (e.g. connection refused)
        print("URLError: {}".format(e.reason))
    else:
        # 200
        print("Success")