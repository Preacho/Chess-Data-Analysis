import pandas as pd 
import sys
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd

def main():
    chess_data_csv_input_list = ['/chess_datascore0-1000Elo.csv', 
                       '/chess_datascore1000-1250Elo.csv',
                       '/chess_datascore1250-1500Elo.csv',
                       '/chess_datascore1500-1750Elo.csv',
                       '/chess_datascore1750-2000Elo.csv',
                       '/chess_datascore2000-2250Elo.csv',
                       '/chess_datascore2250+Elo.csv'
                       ]
    input_directory = sys.argv[1]

    '''chess_data_frames = []
    for input_file in chess_data_csv_input_list:
        df = pd.read_csv(input_directory + input_file)
        df.dropna(subset=['calc_time'], inplace=True)
        chess_data_frames.append(df['calc_time'])'''

    # Load data
    eval_data_frames = []
    for input_file in chess_data_csv_input_list:
        print(input_file)

        df = pd.read_csv(input_directory + input_file)
        df.dropna(subset=['calc_time', 'Calc_Eval'], inplace=True)
        eval_data_frames.append(df[['calc_time', 'Calc_Eval']])

        # Combine all data frames into a single DataFrame for evaluation purposes
        combined_eval_data = pd.concat(eval_data_frames, ignore_index=True)

        # Assign each evaluation score to a group based on calc_time (1 to 300 seconds)
        combined_eval_data = combined_eval_data[combined_eval_data['calc_time'].between(1, 300)]
        combined_eval_data['time_group'] = combined_eval_data['calc_time'].astype(int)

        # Group by 'time_group' and prepare data for ANOVA
        grouped_eval_data = [group['Calc_Eval'].values for _, group in combined_eval_data.groupby('time_group')]

        # ANOVA Test for Differences in Evaluation Scores across 300 time groups
        anova_results_time_groups = stats.f_oneway(*grouped_eval_data)

        # Print ANOVA results for evaluation scores across 300 time groups
        print(f"ANOVA Results for Evaluation Scores Across 300 Time Groups:\nF-statistic: {anova_results_time_groups.statistic}, p-value: {anova_results_time_groups.pvalue} \n")

        # Optional: Check if there are significant differences between groups
        if anova_results_time_groups.pvalue < 0.05:
            print("Significant differences between time groups detected for Evaluation Scores.\n")

    

    # ANOVA Test for Differences in Move Times by Player Elo
    '''anova_results = stats.f_oneway(*chess_data_frames)

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
        print("No significant differences found between Elo ranges.")'''

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        main()
    else: 
        print('Not enough arguments provided.')
