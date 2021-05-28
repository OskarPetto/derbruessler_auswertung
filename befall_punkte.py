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

periods = {
    'Jahr 0 Gesamt': (0, 1, 0, 12),
    'Jahr -1 Gesamt': (-1, 1, -1, 12),
    'Entwickelter Käfer': (-1, 8, 0, 3),
    'Aktiver Käfer': (0, 3, 0, 5),
    'Ei': (-1, 5, -1, 6),
    'Larve': (-1, 5, -1, 8),
    'Puppe': (-1, 7, -1, 9)
}

rr_file_name = 'daten/rr_spartakus_daily_1970-2020_ua_la_vi_bu.nc'
tmean_file_name = 'daten/tmean_spartakus_daily_1970-2020_ua_la_vi_bu.nc'
ruessler_file_name = 'daten/data.csv'

out_file_name = 'daten/befall_punkte.csv'

ruessler_rows = read_rows(ruessler_file_name)
ruessler_rows_filtered = []

tmean_data_array = open_klima_file(tmean_file_name, 'Tmean')
rr_data_array = open_klima_file(rr_file_name, 'RR')
cache = {}

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
    if (latitude, longitude) in cache:
        rr_point = rr_cache[(latitude, longitude)]['RR']
        tmean_point = tmean_cache[(latitude, longitude)]['Tmean']
    else:
        (x, y) = transformer.transform(latitude, longitude)
        rr_point = spacial_slice_point(rr_data_array, x, y, 0)
        tmean_point = spacial_slice_point(tmean_data_array, x, y, 0)
        rr_cache[(latitude, longitude)]['RR'] = rr_point
        rr_cache[(latitude, longitude)]['Tmean'] = rr_point
    row_dict = {'Befallsbewertung': befallsbewertung}
    for period_name, period in periods.items():
        rr_period = temporal_slice(rr_point, jahr + period[0], period[1], jahr + period[2], period[3])
        rr_aggregate = rr_period.where(rr_period != -999).mean().item(0)
        tmean_period = temporal_slice(tmean_point, jahr + period[0], period[1], jahr + period[2], period[3])
        tmean_aggregate = tmean_period.where(tmean_period != -999).mean().item(0)
        row_dict['RR ' + period_name] = rr_aggregate
        row_dict['Tmean ' + period_name] = tmean_aggregate
    out_rows.append(row_dict)

write_rows(out_file_name, out_rows)
