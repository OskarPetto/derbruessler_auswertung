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
    'Jahr Gesamt': (0, 1, 0, 12),
    'Vorjahr Gesamt': (-1, 1, -1, 12),
    'Entwickelter Käfer': (-1, 8, 0, 3),
    'Aktiver Käfer': (0, 3, 0, 5),
    'Aktiver Käfer Vorjahr': (-1, 3, 0, 5),
    'Ei': (-1, 5, -1, 6),
    'Larve': (-1, 5, -1, 8),
    'Puppe': (-1, 7, -1, 9),
}

min_temp = 25
max_rr = 1

shape_file_name = 'daten/Gebiete_AGRANA.shp'
rr_file_name = 'daten/rr_spartakus_daily_1970-2020_ua_la_vi_bu.nc'
tmean_file_name = 'daten/tmean_spartakus_daily_1970-2020_ua_la_vi_bu.nc'
tx_file_name = 'daten/tmax_spartakus_daily_1970-2020_ua_la_vi_bu.nc'
ruessler_file_name = 'daten/data.csv'

out_file_name = 'daten/befall_gesamtgebiet.csv'

ruessler_rows = read_rows(ruessler_file_name)
befall_pro_jahr = befallsbewertung_pro_jahr(ruessler_rows)

rr_data_set = open_klima_file(rr_file_name)
tmean_data_set = open_klima_file(tmean_file_name)
tx_data_set = open_klima_file(tx_file_name)
klima_data_set_all_positions = rr_data_set\
    .merge(tmean_data_set, compat="identical", combine_attrs="identical") \
    .merge(tx_data_set, compat="identical", combine_attrs="identical")
klima_data_set_all_positions.rio.write_crs(rr_data_set.rio.crs, inplace=True)
print(klima_data_set_all_positions)
geodf = geopandas.read_file(shape_file_name)
klima_data_set = spacial_slice_polygon(klima_data_set_all_positions, geodf)

out_rows = []

for year in tqdm(range(start_year, end_year + 1)):
    year_str = str(year)
    befall = 0
    if year_str in befall_pro_jahr:
        befall = befall_pro_jahr[year_str]
    row_dict = {'Jahr': year, 'Befall': befall}
    for period_name, period in periods.items():
        klima_data_set_period = temporal_slice(klima_data_set, year + period[0], period[1], year + period[2], period[3])
        tmean_data_array = klima_data_set_period.data_vars['Tmean'].where(lambda tmean: tmean != -999).mean('x').mean('y')
        tx_data_array = klima_data_set_period.data_vars['Tx'].where(lambda tx: tx != -999).mean('x').mean('y')
        rr_data_array = klima_data_set_period.data_vars['RR'].where(lambda rr: rr != -999).mean('x').mean('y')
        tmean_mean = tmean_data_array.mean().item(0)
        tx_mean = tx_data_array.mean().item(0)
        rr_sum = rr_data_array.sum().item(0)
        summer_day_count = (tx_data_array >= min_temp).sum().item(0) #((tx_data_array >= min_temp) & (rr_data_array <= max_rr)).sum().item(0)
        # print(hot_and_dry_day_count, '/', len(tx_data_array))
        row_dict['mean Tmean ' + period_name] = tmean_mean
        row_dict['sum RR ' + period_name] = rr_sum
        row_dict['#(Tx >= ' + str(min_temp) + ') ' + period_name] = summer_day_count


    out_rows.append(row_dict)

write_rows(out_file_name, out_rows)