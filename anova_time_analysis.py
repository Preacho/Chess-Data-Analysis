import pandas as pd 
import sys
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd

from game_performance import get_game_performance

def main():
    chess_data_csv_input_list = ['/chess_data0-1000Elo.csv', 
                       '/chess_data1000-1250Elo.csv',
                       '/chess_data1250-1500Elo.csv',
                       '/chess_data1500-1750Elo.csv',
                       '/chess_data1750-2000Elo.csv',
                       '/chess_data2000-2250Elo.csv',
                       '/chess_data2250+Elo.csv'
                       ]
    input_directory = sys.argv[1]

    chess_data_frames = []
    for input_file in chess_data_csv_input_list:
        df = pd.read_csv(input_directory + input_file)
        df.dropna(inplace=True)
        game_performance = df.apply(lambda x: get_game_performance(x), axis=1)
        game_performance = pd.concat(game_performance.tolist(), ignore_index=True)
        game_performance = game_performance[game_performance['calc_time'] >= 0]
        chess_data_frames.append(game_performance['calc_time'])

    # ANOVA Test for Differences in Move Times by Player Elo
    anova_results = stats.f_oneway(*chess_data_frames)

    # Print ANOVA results
    print(f"ANOVA Results:\nF-statistic: {anova_results.statistic}, p-value: {anova_results.pvalue}")

    # Check for significance
    if anova_results.pvalue < 0.05:
        print("Significant differences between Elo groups detected.\n")

        # Combine all Elo ranges into a single DataFrame for Tukey's HSD
        combined_data = pd.concat([
            pd.DataFrame({'calc_time': data, 'Elo_Range': [input_file] * len(data)})
            for data, input_file in zip(chess_data_frames, chess_data_csv_input_list)
        ], ignore_index=True)

        # Perform Tukey's HSD for post-hoc analysis
        tukey = pairwise_tukeyhsd(endog=combined_data['calc_time'], groups=combined_data['Elo_Range'], alpha=0.05)

        # Print the results of Tukey's HSD test
        print("Tukey's HSD results:")
        print(tukey)

        # Plot Tukey's HSD result
        tukey.plot_simultaneous()
        plt.title("Tukey HSD: Comparison of Move Times Across Elo Ranges")
        plt.show()
    else:
        print("No significant differences found between Elo ranges.")

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        main()
    else: 
        print('Not enough arguments provided.')
