from collections import defaultdict
import datetime
from dateutil.relativedelta import relativedelta
import rioxarray
from pyproj import CRS, Transformer
import numpy as np


def old_temporal_slice(var_time, var_val, from_date, to_date):
    # time is in days from 1961-01-01
    start_date = datetime.date.fromisoformat('1961-01-01')
    from_days = (from_date - start_date).days
    to_days = (to_date - start_date).days

    if from_days < var_time[0] or to_days > var_time[-1] or from_days > to_days:
        raise Exception('Zeitspanne nicht korrekt oder außerhalb den verfügbaren Daten (1961-01-01-...)')

    index_from_days = int(from_days - var_time[0])
    index_to_days = int(to_days - var_time[0]) + 1

    return var_val[index_from_days:index_to_days, :, :]


def old_spacial_slice_point(var_x, var_y, var_val, latitude, longitude, umkreis):
    from_crs = default_crs()
    to_crs = CRS.from_wkt(var_val.__dict__['esri_pe_string'])

    transformer = Transformer.from_crs(from_crs, to_crs)

    (x, y) = transformer.transform(latitude, longitude)

    if x > var_x[-1] or x < var_x[0] or y > var_y[-1] or x < var_y[0]:
        raise Exception('Koordinate ist außerhalb der verfügbaren Daten')

    index_x = binary_search_closest(var_x, x)
    index_y = binary_search_closest(var_y, y)

    index_from_x = index_x - umkreis
    index_to_x = index_x + umkreis + 1
    index_from_y = index_y - umkreis
    index_to_y = index_y + umkreis + 1

    if index_from_x < 0 or index_to_x > len(var_x) or index_from_y < 0 or index_to_y > len(var_y):
        raise Exception('Umkreis ist zu groß')

    return var_val[:, index_from_y:index_to_y, index_from_x:index_to_x]


def count_aggregate(rows, keys=None):
    if keys is None:
        keys = []
    aggregate = defaultdict(int)
    for row in rows:
        aggregate_key = []
        for key in keys:
            aggregate_key.append(row[key].lower())
        aggregate_key_str = '|'.join(aggregate_key)
        aggregate[aggregate_key_str] += 1
    return aggregate


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


def temporal_slice(data_set, from_date, to_date):
    return data_set.sel(time=slice(from_date, to_date))


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
def spacial_slice_polygon(data_set, shape):
    pass
