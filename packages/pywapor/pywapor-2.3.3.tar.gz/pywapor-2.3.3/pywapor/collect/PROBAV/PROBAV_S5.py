import sys
from pathlib import Path
from pywapor.collect.PROBAV.DataAccess import download_data
import pywapor
import glob
import os

def main(download_dir, latitude_extent, longitude_extent, start_date, end_date, 
        buffer_dates = True):
    """

    """
    username, password = pywapor.collect.get_pw_un.get("VITO")

    download_data(download_dir/Path("PROBAV"), start_date, end_date, latitude_extent,
                  longitude_extent, username, password, buffer_dates = buffer_dates)

    albedo_files = glob.glob(os.path.join(download_dir, "PROBAV", "Albedo", "Albedo*.tif"))
    ndvi_files = glob.glob(os.path.join(download_dir, "PROBAV", "NDVI", "NDVI*.tif"))

    return ndvi_files, albedo_files

if __name__ == '__main__':
    main(sys.argv)

#     download_dir = r"/Users/hmcoerver/On My Mac/probav_test"
#     latitude_extent = [28.9, 29.7]
#     longitude_extent = [30.2, 31.2]
#     start_date = "2021-07-05"
#     end_date = "2021-07-05"

#     main(download_dir, latitude_extent, longitude_extent, start_date, end_date, 
#         buffer_dates = True)
