import geopandas
from netCDF4 import Dataset
from pyproj import CRS, Transformer
import numpy as np
import datetime
from tqdm import tqdm
from csv_io import *
import matplotlib.pyplot as plt
from datenauswertung import *
import math

periods = [(-1, 5, 9), (-1, 5, 7), (0, 4, 5)]

rr_file_name = 'daten/rr_spartakus_daily_1970-2020_ua_la_vi_bu.nc'
ruessler_file_name = 'daten/data.csv'

out_file_name = 'daten/befall_rr.csv'

ruessler_rows = read_rows(ruessler_file_name)
ruessler_rows_filtered = []

rr_data_array = open_klima_file(rr_file_name, 'RR')
rr_cache = {}

from_crs = CRS.from_epsg(4326)  # https://en.wikipedia.org/wiki/World_Geodetic_System
to_crs = rr_data_array.rio.crs
transformer = Transformer.from_crs(from_crs, to_crs)

out_rows = []

for row in ruessler_rows:
    jahr = int(row['Jahr'])
    latitude = unlocalize_float(row['Latitude'])
    longitude = unlocalize_float(row['Longitude'])
    befall = row['Befall'].lower().strip()
    if not math.isnan(latitude) and not math.isnan(longitude) and befall == 'ja':
        befallsbewertung = row['Befallsbewertung']
        ruessler_rows_filtered.append({'Jahr': jahr, 'Latitude': latitude, 'Longitude': longitude, 'Befallsbewertung': befallsbewertung})

for row in tqdm(ruessler_rows_filtered):
    jahr = int(row['Jahr'])
    latitude = row['Latitude']
    longitude = row['Longitude']
    befallsbewertung = row['Befallsbewertung']
    if (latitude, longitude) in rr_cache:
        rr_point = rr_cache[(latitude, longitude)]
    else:
        (x, y) = transformer.transform(latitude, longitude)
        rr_point = spacial_slice_point(rr_data_array, x, y, 0)
        rr_cache[(latitude, longitude)] = rr_point
    row_dict = {'Befallsbewertung': befallsbewertung}
    for period in periods:
        period_name = str(period)
        rr_point_period_data_array = temporal_slice(rr_point, jahr + period[0], period[1], period[2])
        rr_point_period = rr_point_period_data_array.where(rr_point_period_data_array != -999).sum('time')
        rr_point_period_value = rr_point_period.item(0)
        row_dict[period_name] = rr_point_period_value
    out_rows.append(row_dict)

write_rows(out_file_name, out_rows)