import pandas as pd
import os
import sys
from scipy.stats import mannwhitneyu

def main():
    input_directory = sys.argv[1]

    chess_data_csv_list = [
        'chess_datascore0-1000Elo.csv',
        'chess_datascore1000-1250Elo.csv',
        'chess_datascore1250-1500Elo.csv',
        'chess_datascore1500-1750Elo.csv',
        'chess_datascore1750-2000Elo.csv',
        'chess_datascore2000-2250Elo.csv',
        'chess_datascore2250+Elo.csv'
    ]

    threshold = 30  # Example threshold for "short" vs "long" decision times

    # Iterate through each CSV file to perform the Mann-Whitney U test
    for csv_file in chess_data_csv_list:
        file_path = os.path.join(input_directory, csv_file)
        df = pd.read_csv(file_path)

        # Separate data for White and Black players
        white_data = df[df['Player'] == 1]
        black_data = df[df['Player'] == 0]

        # Separate groups based on calc_time threshold for White players
        white_short_time_group = white_data[white_data['calc_time'] < threshold]['Improvement']
        white_long_time_group = white_data[white_data['calc_time'] >= threshold]['Improvement']

        # Separate groups based on calc_time threshold for Black players
        black_short_time_group = -black_data[black_data['calc_time'] < threshold]['Improvement']
        black_long_time_group = -black_data[black_data['calc_time'] >= threshold]['Improvement']

        # Perform Mann-Whitney U test on short vs long decision times for White players
        if not white_short_time_group.empty and not white_long_time_group.empty:
            u_stat, p_value = mannwhitneyu(white_short_time_group, white_long_time_group, alternative='two-sided')
            print(f"Mann-Whitney U Test (White Short vs Long Decision Times) for {csv_file}: U-statistic = {u_stat:.3f}, p-value = {p_value:.50f}")

        # Perform Mann-Whitney U test on short vs long decision times for Black players
        if not black_short_time_group.empty and not black_long_time_group.empty:
            u_stat, p_value = mannwhitneyu(black_short_time_group, black_long_time_group, alternative='two-sided')
            print(f"Mann-Whitney U Test (Black Short vs Long Decision Times) for {csv_file}: U-statistic = {u_stat:.3f}, p-value = {p_value:.50f}")

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        main()
    else:
        print('Not enough arguments provided.')
