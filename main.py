import pandas as pd
import glob
import matplotlib.pyplot as plt
import os
import sys
from datetime import datetime

import format_data as formatter


def read_all_data(game: str):
    path_raw = 'data/' + game + '/raw'
    all_raw_files = glob.glob(path_raw + '/*.csv')
    for filename in all_raw_files:
        day = filename.split('/')[-1].split('.')[0]
        formatter.format_file(game, day)

    path = 'data/' + game + '/formatted'
    all_files = glob.glob(path + '/*.csv')
    all_data = []

    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0)
        my_dict = {filename.split('/')[3].split('.')[0]: df}
        all_data.append(my_dict)

    return all_data


def read_single_data(filename):
    df = pd.read_csv(filename, index_col=None, header=0)
    return df


def get_player_columns(chosen_dataframe: pd.DataFrame):
    return [player_columns for player_columns in chosen_dataframe.columns if 'Spieler' in player_columns]


def get_min(chosen_dataframe: pd.DataFrame):
    player_columns = get_player_columns(chosen_dataframe)

    minimum = chosen_dataframe[player_columns[0]].min()

    for column in player_columns:
        new_minimum = chosen_dataframe[column].min()
        if new_minimum < minimum:
            minimum = new_minimum

    return minimum


def get_max(chosen_dataframe: pd.DataFrame):
    player_columns = get_player_columns(chosen_dataframe)

    maximum = chosen_dataframe[player_columns[0]].max()

    for column in player_columns:
        new_maximum = chosen_dataframe[column].max()
        if new_maximum > maximum:
            maximum = new_maximum

    return maximum


def create_plot_for_all_days(game: str):
    data = read_all_data(game)
    days = []

    plt.xlabel('Spieltag')
    plt.ylabel('Punkte')
    plt.title('Skatspiele')

    for elem in data:
        for key, value in elem.items():
            days.append(key)

            for player in get_player_columns(value):
                player_name = player.split(' - ')[1]
                if counter:
                    player_result = value[player].astype(bool).sum(axis=0)
                else:
                    player_result = value[player].iloc[-1]
                plt.scatter(key, player_result, label=player_name)

    days.sort(key=lambda date: datetime.strptime(date, '%d-%m-%Y'))
    plt.xticks(days)
    plt.legend()
    plt.savefig('data/' + game + '/diagramms/' + 'all_data', dpi=300)
    plt.show()


def create_plot_for_day(game: str, day: str):
    formatter.format_file(game, day)
    file = 'data/' + game + '/formatted/' + day + '.csv'
    df = read_single_data(file)
    min_y = get_min(df)
    max_y = get_max(df)
    min_x = df['Spielnummer'].min()
    max_x = df['Spielnummer'].max()

    plt.axis([min_x, max_x, min_y, max_y])
    plt.xlabel('Spiel')
    plt.ylabel('Punkte')
    plt.title('Skat Spiel am ' + day)
    for player in get_player_columns(df):
        player_name = player.split(' - ')[1]
        if counter:
            player_result = df[player].astype(bool)
        else:
            player_result = df[player]
        plt.plot(df['Spielnummer'], player_result, label=player_name)
    plt.legend()
    plt.savefig('data/' + game + '/diagramms/' + day, dpi=72)
    plt.show()


def create_diagramm_folder(game: str):
    directory_created = os.path.isdir('data/' + game + '/diagramms')
    if not directory_created:
        os.mkdir('data/' + game + '/diagramms')


def main():
    global counter

    game = ''
    counter = False
    date = ''

    if len(sys.argv) == 1:
        print('Specifiy parameters.')
        return

    for i in range(1, len(sys.argv)):
        parameter = sys.argv[i]
        if '-g' in parameter:
            game = parameter.split('=')[1]
        elif '-c' in parameter:
            counter = True
        elif '-d' in parameter:
            date = parameter.split('=')[1]

    create_diagramm_folder(game)

    if not date:
        create_plot_for_all_days(game)
    else:
        create_plot_for_day(game, date)


if __name__ == '__main__':
    main()
