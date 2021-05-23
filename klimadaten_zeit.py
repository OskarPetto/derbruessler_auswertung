import geopandas
from netCDF4 import Dataset
from pyproj import CRS, Transformer
import numpy as np
import datetime
from tqdm import tqdm
from csv_io import read_rows, rows_to_columns
import matplotlib.pyplot as plt
from datenauswertung import *

start_year = 1980
end_year = 2021

shape_file_name = 'daten/Gebiete_AGRANA.shp'
rr_file_name = 'daten/rr_spartakus_daily_1970-2020_ua_la_vi_bu.nc'
tmean_file_name = 'daten/tmean_spartakus_daily_1970-2020_ua_la_vi_bu.nc'
ruessler_file_name = 'daten/coordinates.csv'


ruessler_rows = read_rows(ruessler_file_name)
print(sum_aggregate(ruessler_rows, "Jahr", "Befallsstärke"))



# from_crs = CRS.from_epsg(4326)  # https://en.wikipedia.org/wiki/World_Geodetic_System
# rr_data_set = open_klima_file(rr_file_name)
# to_crs = rr_data_set.rio.crs
# transformer = Transformer.from_crs(from_crs, to_crs)

#
# latitude = 48.228082690619544
# longitude = 16.689064484415454
# (x, y) = transformer.transform(latitude, longitude)
#
#
# rr_data_set = spacial_slice_point(rr_data_set, x, y, 1)
#
# print(rr_data_set)


# rr_data_set = temporal_slice(rr_data_set, "2020-03-01", "2020-03-01")
#
# geodf = geopandas.read_file(shape_file_name)
# clipped = spacial_slice_polygon(rr_data_set, geodf)
#
# clipped['RR'].plot()
# plt.show()


