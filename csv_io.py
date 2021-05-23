import csv
from collections import defaultdict


def read_rows(csv_file):
    rows = []
    with open(csv_file, encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            rows.append(row)
    return rows


def rows_to_columns(rows):
    keys = list(rows[0].keys())
    columns = defaultdict(list)
    for row in rows:
        for key in keys:
            columns[key].append(row[key])
    return columns


# https://stackoverflow.com/questions/39833555/how-to-write-a-csv-with-a-comma-as-the-decimal-separator
def localize_floats(row):
    return {k: str(v).replace('.', ',') if isinstance(v, float) else str(v) for k, v in row.items()}


def write_rows(csv_file, rows):
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = rows[0].keys()
        writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=fieldnames)

        writer.writeheader()
        for row in rows:
            writer.writerow(localize_floats(row))


def is_useless(value):
    return value == '' or value == '#NV'
