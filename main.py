import pandas as pd
import glob
import matplotlib.pyplot as plt

list_day = []

def read_data():
    path = 'data/formatted'
    all_files = glob.glob(path + '/*.csv')

    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0)
        list_day.append(df)

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

def main():
    read_data()
    #print(list_day)
    #print(len(list_day))

    print(list_day[0])

    print(get_min(list_day[0]))
    print(get_max(list_day[0]))

if __name__ == '__main__':
   main()

