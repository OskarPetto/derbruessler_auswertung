from csv_io import read_rows, write_rows

befallstaerke_values = {
    'nein': 0,
    'ka': 1,
    'gering': 1,
    'mittel': 2,
    'schwer': 3,
    'stark': 3,
    'mittel-stark': 2.5
}

umbruch_values = {
    'nein': 0,
    '': 0,
    'ka': 0,
    'teilumbruch': 0.5,
    'ja': 0.5,
    'gesamtumbruch': 1
}

allowed_befallstaerke = set(befallstaerke_values.keys())
allowed_umbruch = set(umbruch_values.keys())


def bewerte_befall(befallstaerke, umbruch):

    if befallstaerke not in allowed_befallstaerke:
        raise Exception('Kenne Befallstärke \"' + befallstaerke + '\" nicht')

    if umbruch not in allowed_umbruch:
        raise Exception('Kenne Umbruch \"' + umbruch + '\" nicht')

    return befallstaerke_values[befallstaerke]  # + umbruch_values[umbruch]


in_file_name = 'daten/data.csv'
out_file_name = 'daten/data.csv'

rows = read_rows(in_file_name)

for row in rows:
    befallstaerke = row['Schwere des Befalls (Einschätzung)'].lower()
    umbruch = row['Flächenumbruch'].lower()
    row['Befallsbewertung'] = bewerte_befall(befallstaerke, umbruch)

write_rows(out_file_name, rows)

