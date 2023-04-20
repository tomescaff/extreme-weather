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

PYTHON_USER_AGENT="python/" + PYTHON_VERSION + "/esg/4.3.1-20230321-173145/created/2023-03-31T12:22:37-06:00"

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
# Usage: python3 python-ucar.cgd.ccsm4.cesmLE.atm.proc.monthly_ave.TREFHT-20230331T1222Z.py
# Version: 0.1.0-alpha
#
#
# Dataset
# ucar.cgd.ccsm4.cesmLE.atm.proc.monthly_ave.TREFHT
# 95f83363-4bd0-4ab3-94a2-0267651e46d5
# https://www.earthsystemgrid.org/dataset/ucar.cgd.ccsm4.cesmLE.atm.proc.monthly_ave.TREFHT.html
# https://www.earthsystemgrid.org/dataset/id/95f83363-4bd0-4ab3-94a2-0267651e46d5.html
#
# Dataset Version
# 2
# 9c4dfd30-8927-4130-8658-8a210705bfef
# https://www.earthsystemgrid.org/dataset/ucar.cgd.ccsm4.cesmLE.atm.proc.monthly_ave.TREFHT/version/2.html
# https://www.earthsystemgrid.org/dataset/version/id/9c4dfd30-8927-4130-8658-8a210705bfef.html
#
################################################################

print("This Python 3 download script is experimental.  Please provide feedback at 'esg-support@earthsystemgrid.org'.")
print("")

urls = [
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/monthly/TREFHT/b.e11.B1850C5CN.f09_g16.005.cam.h0.TREFHT.040001-049912.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/monthly/TREFHT/b.e11.B1850C5CN.f09_g16.005.cam.h0.TREFHT.050001-059912.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/monthly/TREFHT/b.e11.B1850C5CN.f09_g16.005.cam.h0.TREFHT.060001-069912.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/monthly/TREFHT/b.e11.B1850C5CN.f09_g16.005.cam.h0.TREFHT.070001-079912.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/monthly/TREFHT/b.e11.B1850C5CN.f09_g16.005.cam.h0.TREFHT.080001-089912.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/monthly/TREFHT/b.e11.B1850C5CN.f09_g16.005.cam.h0.TREFHT.090001-099912.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/monthly/TREFHT/b.e11.B1850C5CN.f09_g16.005.cam.h0.TREFHT.100001-109912.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/monthly/TREFHT/b.e11.B1850C5CN.f09_g16.005.cam.h0.TREFHT.110001-119912.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/monthly/TREFHT/b.e11.B1850C5CN.f09_g16.005.cam.h0.TREFHT.120001-129912.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/monthly/TREFHT/b.e11.B1850C5CN.f09_g16.005.cam.h0.TREFHT.130001-139912.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/monthly/TREFHT/b.e11.B1850C5CN.f09_g16.005.cam.h0.TREFHT.140001-149912.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/monthly/TREFHT/b.e11.B1850C5CN.f09_g16.005.cam.h0.TREFHT.150001-159912.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/monthly/TREFHT/b.e11.B1850C5CN.f09_g16.005.cam.h0.TREFHT.160001-169912.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/monthly/TREFHT/b.e11.B1850C5CN.f09_g16.005.cam.h0.TREFHT.170001-179912.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/monthly/TREFHT/b.e11.B1850C5CN.f09_g16.005.cam.h0.TREFHT.180001-189912.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/monthly/TREFHT/b.e11.B1850C5CN.f09_g16.005.cam.h0.TREFHT.190001-199912.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/monthly/TREFHT/b.e11.B1850C5CN.f09_g16.005.cam.h0.TREFHT.200001-209912.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF',
     'https://tds.ucar.edu/thredds/fileServer/datazone/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/monthly/TREFHT/b.e11.B1850C5CN.f09_g16.005.cam.h0.TREFHT.210001-220012.nc?api-token=Gu6m2qV0xQkj1DGc11kbkEOeqcbcCa4VXlKXlYzF']

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
        file_name = os.path.join('/home/tcarrasco/result/data/LENS1/tas/orig/CR/', file_name)
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