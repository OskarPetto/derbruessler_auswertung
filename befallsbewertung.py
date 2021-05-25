from csv_io import read_rows, write_rows

befallstaerke_values = {
    'nein': 0,
    'gering': 1,
    'mittel': 2,
    'schwer': 3,
    'stark': 3,
    'mittel-stark': 2.5
}

none_values = {'ka'}
allowed_befallstaerke = set(befallstaerke_values.keys()).union(none_values)


def bewerte_befall(befallstaerke):

    if befallstaerke not in allowed_befallstaerke:
        raise Exception('Kenne Befallstärke \"' + befallstaerke + '\" nicht')

    if befallstaerke in none_values:
        return 1

    return befallstaerke_values[befallstaerke]


in_file_name = 'daten/data.csv'
out_file_name = 'daten/data.csv'

rows = read_rows(in_file_name)

for row in rows:
    befallstaerke = row['Schwere des Befalls (Einschätzung)'].lower()
    row['Befallsbewertung'] = bewerte_befall(befallstaerke)

write_rows(out_file_name, rows)

