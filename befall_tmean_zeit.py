import geopandas
from netCDF4 import Dataset
from pyproj import CRS, Transformer
import numpy as np
import datetime
from tqdm import tqdm
from csv_io import read_rows, write_rows, rows_to_columns
import matplotlib.pyplot as plt
from datenauswertung import *

start_year = 1980
end_year = 2020

shape_file_name = 'daten/Gebiete_AGRANA.shp'
tmean_file_name = 'daten/tmean_spartakus_daily_1970-2020_ua_la_vi_bu.nc'
ruessler_file_name = 'daten/data.csv'

out_file_name = 'daten/befall_tmean_zeit.csv'

ruessler_rows = read_rows(ruessler_file_name)
befall_pro_jahr = befallsbewertung_pro_jahr(ruessler_rows)

tmean_data_array = open_klima_file(tmean_file_name, 'Tmean')
geodf = geopandas.read_file(shape_file_name)
tmean_gebiete = spacial_slice_polygon(tmean_data_array, geodf)

out_rows = []

for year in range(start_year, end_year + 1):
    tmean_jahr_data_array = temporal_slice(tmean_gebiete, year, 1, 12)
    tmean_jahr = tmean_jahr_data_array.where(tmean_jahr_data_array != -999).mean()
    tmean_jahr_value = tmean_jahr.item(0)
    year_str = str(year)
    befall = 0
    if year_str in befall_pro_jahr:
        befall = befall_pro_jahr[str(year)]
    out_rows.append({'Jahr': year, 'Befall': befall, 'Tmean': tmean_jahr_value})

write_rows(out_file_name, out_rows)


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
