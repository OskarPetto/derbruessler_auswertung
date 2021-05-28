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

periods = {
    'Jahr 0 Gesamt': (0, 1, 0, 12),
    'Jahr -1 Gesamt': (-1, 1, -1, 12),
    'Entwickelter Käfer': (-1, 8, 0, 3),
    'Aktiver Käfer': (0, 3, 0, 5),
    'Ei': (-1, 5, -1, 6),
    'Larve': (-1, 5, -1, 8),
    'Puppe': (-1, 7, -1, 9)
}


shape_file_name = 'daten/Gebiete_AGRANA.shp'
rr_file_name = 'daten/rr_spartakus_daily_1970-2020_ua_la_vi_bu.nc'
tmean_file_name = 'daten/tmean_spartakus_daily_1970-2020_ua_la_vi_bu.nc'
ruessler_file_name = 'daten/data.csv'

out_file_name = 'daten/befall_gesamtgebiet.csv'

ruessler_rows = read_rows(ruessler_file_name)
befall_pro_jahr = befallsbewertung_pro_jahr(ruessler_rows)

rr_data_array = open_klima_file(rr_file_name, 'RR')
tmean_data_array = open_klima_file(tmean_file_name, 'Tmean')
geodf = geopandas.read_file(shape_file_name)
rr_gebiete = spacial_slice_polygon(rr_data_array, geodf)
tmean_gebiete = spacial_slice_polygon(tmean_data_array, geodf)

out_rows = []

for year in tqdm(range(start_year, end_year + 1)):
    year_str = str(year)
    befall = 0
    if year_str in befall_pro_jahr:
        befall = befall_pro_jahr[year_str]
    row_dict = {'Jahr': year, 'Befall': befall}
    for period_name, period in periods.items():
        rr_period = temporal_slice(rr_gebiete, year + period[0], period[1], year + period[2], period[3])
        rr_period = rr_period.where(rr_period != -999)
        tmean_period = temporal_slice(tmean_gebiete, year + period[0], period[1], year + period[2], period[3])
        tmean_period = tmean_period.where(tmean_period != -999)
        rr_aggregate = rr_period.mean().item(0)
        tmean_aggregate = tmean_period.mean().item(0)
        quotient_aggregate = rr_aggregate / tmean_aggregate
        row_dict['RR ' + period_name] = rr_aggregate
        row_dict['Tmean ' + period_name] = tmean_aggregate
        row_dict['RR/Tmean ' + period_name] = quotient_aggregate
    out_rows.append(row_dict)

write_rows(out_file_name, out_rows)