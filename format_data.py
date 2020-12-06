import csv
import os

data_dict = {}
headers = []


def read_to_dict(file: str):
    global headers
    with open(file) as data:
        csv_reader = csv.reader(data, delimiter=',')
        headers = next(csv_reader)
        dict_reader = csv.DictReader(data, fieldnames=headers)
        line_count = 0
        for record in dict_reader:
            data_dict[line_count] = record
            line_count += 1


def replace_hyphen_all_columns():
    player_columns = [players for players in headers if 'Spieler' in players]
    for column in player_columns:
        replace_hyphen(column)


def replace_hyphen(column: str):
    for key, data in data_dict.items():
        if data[column] == '-':
            previous_entry = get_previous_entry(key - 1, column)
            data[column] = previous_entry


def get_previous_entry(key: int, column: str):
    if key == -1:
        key = 0
    entry = data_dict[key][column]
    if key == 0:
        if entry != '-':
            return entry
        else:
            return 0
    else:
        if entry != '-':
            return entry
        else:
            return get_previous_entry(key - 1, column)


def write_to_csv(file: str):
    directory_list = file.split('/')
    directory = directory_list[0] + '/' + directory_list[1] + '/formatted'
    directory_created = os.path.isdir(directory)
    if not directory_created:
        os.mkdir(directory)

    with open(directory + '/' + get_filename(file), 'w+') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)

        writer.writeheader()
        for i in range(0, len(data_dict.items())):
            writer.writerow(data_dict[i])


def get_filename(file: str):
    return file.split('/')[3]


def format_file(game: str, day: str):
    file = 'data/' + game + '/raw/' + day + '.csv'
    read_to_dict(file)
    replace_hyphen_all_columns()
    write_to_csv(file)
