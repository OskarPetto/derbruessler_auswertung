from collections import defaultdict
import datetime
from dateutil.relativedelta import relativedelta
import rioxarray
from pyproj import CRS, Transformer
import numpy as np
from shapely.geometry import mapping


def befallsbewertung_pro_jahr(rows):
    agg = defaultdict(list)
    for row in rows:
        key_val = row['Jahr']
        val_val = float(row['Befallsbewertung'].replace(',', '.'))
        if val_val != 0:
            agg[key_val].append(val_val)

    return {k: sum(v) / len(v) for k, v in agg.items()}


def binary_search_closest(data, value):
    low = 0
    high = len(data) - 1
    best_index = low
    desc_factor = 1
    if data[low] > data[high]:
        desc_factor = -1
    desc_value = desc_factor * value
    while low <= high:
        mid = (high + low) // 2
        desc_mid = data[mid] * desc_factor
        if desc_mid < desc_value:
            low = mid + 1
        elif desc_mid > desc_value:
            high = mid - 1
        else:
            best_index = mid
            break
        if abs(data[mid] - value) < abs(data[best_index] - value):
            best_index = mid
    return best_index


def date_to_months(date):
    start_date = datetime.date.fromisoformat('1961-01-01')
    return relativedelta(start_date, date).months


def default_crs():
    return CRS.from_epsg(4326)  # https://en.wikipedia.org/wiki/World_Geodetic_System


def open_klima_file(file_name):
    data_set = rioxarray.open_rasterio(file_name)
    return data_set.sel(band=1)


def temporal_slice(data_set, year, from_month, to_month):
    data_years = data_set['time.year']
    data_months = data_set['time.month']
    year_mask = data_years == year
    month_mask = (data_months >= from_month) & (data_months <= to_month)
    mask = year_mask & month_mask
    return data_set.sel(time=mask)


def spacial_slice_point(data_set, x, y, umkreis):

    index_x = binary_search_closest(data_set.x.values, x)
    index_y = binary_search_closest(data_set.y.values, y)

    index_from_x = index_x - umkreis
    index_to_x = index_x + umkreis + 1
    index_from_y = index_y - umkreis
    index_to_y = index_y + umkreis + 1

    return data_set.isel(x=slice(index_from_x, index_to_x), y=slice(index_from_y, index_to_y))


# https://gis.stackexchange.com/questions/354782/how-to-mask-netcdf-time-series-data-from-a-shapefile-in-python
# https://gis.stackexchange.com/questions/264332/clip-a-netcdf-file-using-a-shapefile-with-python
# https://gis.stackexchange.com/questions/289775/masking-netcdf-data-using-shapefile-xarray-geopandas
def spacial_slice_polygon(data_set, geodf):
    polygons = geodf.geometry.apply(mapping)
    clipped = data_set.rio.clip(polygons, geodf.crs, drop=False)
    return clipped
