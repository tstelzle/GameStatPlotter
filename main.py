import pandas as pd
import glob
import matplotlib.pyplot as plt
import os
import sys
from datetime import datetime

import format_data as formatter


def read_all_data():
    path = 'data/formatted'
    all_files = glob.glob(path + '/*.csv')
    all_data = []

    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0)
        my_dict = {filename.split('/')[2].split('.')[0]: df}
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


def create_plot_for_all_days():
    data = read_all_data()
    days = []

    plt.xlabel('Spieltag')
    plt.ylabel('Punkte')
    plt.title('Skatspiele')

    for elem in data:
        for key, value in elem.items():
            days.append(key)

            for player in get_player_columns(value):
                player_name = player.split(' - ')[1]
                player_result = value[player].iloc[-1]
                plt.scatter(key, player_result, label=player_name)

    days.sort(key=lambda date: datetime.strptime(date, '%d-%m-%Y'))
    plt.xticks(days)
    plt.legend()
    plt.savefig('data/diagramms/' + 'all_data', dpi=300)
    plt.show()


def create_plot_for_day(day: str):
    formatter.format_file(day)
    file = 'data/formatted/' + day + '.csv'
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
        plt.plot(df['Spielnummer'], df[player], label=player_name)
    plt.legend()
    plt.savefig('data/diagramms/' + day, dpi=72)
    plt.show()


def create_diagramm_folder():
    directory_created = os.path.isdir('data/diagramms')
    if not directory_created:
        os.mkdir('data/diagramms')


def main():
    create_diagramm_folder()

    if len(sys.argv) == 1:
        create_plot_for_all_days()
    elif len(sys.argv) == 2:
        filename = sys.argv[1]
        create_plot_for_day(filename)
    else:
        print('Too many options.')
        return


if __name__ == '__main__':
    main()
