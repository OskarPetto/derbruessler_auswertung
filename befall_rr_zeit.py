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
ruessler_file_name = 'daten/data.csv'

out_file_name = 'daten/befall_rr_zeit.csv'

ruessler_rows = read_rows(ruessler_file_name)
befall_pro_jahr = befallsbewertung_pro_jahr(ruessler_rows)

rr_data_set = open_klima_file(rr_file_name)
geodf = geopandas.read_file(shape_file_name)
rr_gebiete = spacial_slice_polygon(rr_data_set, geodf)

out_rows = []

for year in range(start_year, end_year):
    year_str = str(year)
    for month in range(1, 13):
        rr_monat_data_set = temporal_slice(rr_gebiete, year, month, month)
        rr_monat = rr_monat_data_set.where(rr_monat_data_set != -999).sum('time').mean('x').mean('y')
        befall = 0
        if month == 4 and year_str in befall_pro_jahr:
            befall = befall_pro_jahr[str(year)]
        out_rows.append({'Jahr': year, 'Monat': month, 'Befall': befall, 'RR': rr_monat})

write_rows(out_rows)


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