import geopandas
from netCDF4 import Dataset
from pyproj import CRS, Transformer
import numpy as np
import datetime
from tqdm import tqdm
from csv_io import read_rows, rows_to_columns
from datenauswertung import *

shape_file_name = 'daten/Gebiete_AGRANA.shp'
rr_file_name = 'daten/rr_spartakus_daily_1970-2020_ua_la_vi_bu.nc'
tmean_file_name = 'daten/tmean_spartakus_daily_1970-2020_ua_la_vi_bu.nc'
ruessler_file_name = 'daten/coordinates.csv'

from_crs = CRS.from_epsg(4326)  # https://en.wikipedia.org/wiki/World_Geodetic_System

shapes = geopandas.read_file(shape_file_name, from_crs)

print(shapes)

# rr_data_set = open_klima_file(rr_file_name)
# to_crs = rr_data_set.rio.crs
# transformer = Transformer.from_crs(from_crs, to_crs)
#
# latitude = 48.228082690619544
# longitude = 16.689064484415454
# (x, y) = transformer.transform(latitude, longitude)
#
#
# rr_data_set = temporal_slice(rr_data_set, "2020-03-01", "2020-03-01")
# rr_data_set = spacial_slice_point(rr_data_set, x, y, 1)
#
# print(rr_data_set)

#
# tmean_file = Dataset(tmean_file_name, "r", format="NETCDF4")
# tmean_var_time = tmean_file.variables['time']
# tmean_var_x = tmean_file.variables['x']
# tmean_var_y = tmean_file.variables['y']
# tmean_var_val = tmean_file.variables['Tmean']
# tmean_crs = CRS.from_wkt(tmean_var_val.__dict__['esri_pe_string'])
# tmean_transformer = Transformer.from_crs(from_crs, tmean_crs)
#
# ruessler_rows = read_rows(ruessler_file_name)
# ruessler_columns = rows_to_columns(ruessler_rows)
#
# print(ruessler_columns['Jahr'])
#
# ruessler_zeit = list(map(lambda jahr: date_to_months(datetime.date(int(jahr), 4, 1)), ruessler_columns['Jahr']))
#
#
# print(ruessler_zeit)
#
# rr_file.close()
# tmean_file.close()

