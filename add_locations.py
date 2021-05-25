from collections import defaultdict

from csv_io import read_rows, write_rows
import pgeocode

coordinate_cache = defaultdict(list)
pgeo_austria = pgeocode.Nominatim('at')


def get_coordinates(plz):
    if plz not in coordinate_cache:
        pgeo_plz = pgeo_austria.query_postal_code(plz)
        coordinate_cache[plz].append(pgeo_plz['latitude'])
        coordinate_cache[plz].append(pgeo_plz['longitude'])
    return coordinate_cache[plz][0], coordinate_cache[plz][1]


in_file_name = 'daten/data.csv'
out_file_name = 'daten/data.csv'

rows = read_rows(in_file_name)

for row in rows:
    plz = row['Postleitzahl']
    latitude, longitude = get_coordinates(plz)
    row['Latitude'] = latitude
    row['Longitude'] = longitude

write_rows(out_file_name, rows)
