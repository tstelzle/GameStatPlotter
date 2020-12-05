import pandas as pd
import glob
import matplotlib.pyplot as plt
import os

import format_data as formatter

list_day = []


def read_all_data():
    path = 'data/formatted'
    all_files = glob.glob(path + '/*.csv')

    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0)
        list_day.append(df)


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
    create_plot_for_day('04-12-2020')


if __name__ == '__main__':
    main()
