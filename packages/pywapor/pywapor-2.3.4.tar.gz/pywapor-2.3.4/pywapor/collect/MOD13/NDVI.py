import sys
from pywapor.collect.MOD13.DataAccess import DownloadData
from datetime import date
import glob
import os
import pywapor

def main(Dir, latlim, lonlim, Startdate, Enddate, Waitbar = 1, 
        hdf_library = None, remove_hdf = 1, buffer_dates = True):

    """
    This function downloads MOD13 16-daily data for the specified time
    interval, and spatial extent.

    Keyword arguments:
    Dir -- 'C:/file/to/path/'
    Startdate -- 'yyyy-mm-dd' or datetime.date
    Enddate -- 'yyyy-mm-dd' or datetime.date
    latlim -- [ymin, ymax]
    lonlim -- [xmin, xmax]
    username -- "" string giving the username of your NASA account (https://urs.earthdata.nasa.gov/)
    password -- "" string giving the password of your NASA account    
    Waitbar -- 1 (Default) will print a waitbar
    hdf_library -- string, if all the hdf files are already stored on computer
                    define directory to the data here
    remove_hdf -- 1 (Default), if 1 remove all the downloaded hdf files in the end    
    """
    if isinstance(Startdate, date):
        Startdate = Startdate.strftime("%Y-%m-%d")
    
    if isinstance(Enddate, date):
        Enddate = Enddate.strftime("%Y-%m-%d")
    
    username, password = pywapor.collect.get_pw_un.get("NASA")

    print('\nDownload 16-daily MOD13 NDVI data for period %s till %s' %(Startdate, Enddate))
    DownloadData(Dir, Startdate, Enddate, latlim, lonlim, username, password, 
                Waitbar, hdf_library, remove_hdf, buffer_dates = buffer_dates)

    return glob.glob(os.path.join(Dir, "MODIS", "MOD13", "*.tif"))

if __name__ == '__main__':
    main(sys.argv) 