import pandas as pd 
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from itertools import combinations
from sklearn.preprocessing import StandardScaler
import os

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
    output_directory = sys.argv[2]
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        
    '''chess_data_frames = []
    for input_file in chess_data_csv_input_list:
        df = pd.read_csv(input_directory + input_file)
        df.dropna(subset=['calc_time'], inplace=True)
        chess_data_frames.append(df['calc_time'])'''

    
    for input_file in chess_data_csv_input_list:

        df = pd.read_csv(input_directory + input_file)
        

        # Assign each evaluation score to a group based on calc_time (1 to 300 seconds)
        df = df[df['calc_time'].between(0,21)]
        df['Calc_Eval'] = df.apply(lambda x: x['Calc_Eval'].astype(float) * -1.0 if x['Player'] == 0.0 else x['Calc_Eval'].astype(float), axis = 1)
        
        
        grouped_eval_data = [group['Calc_Eval'].values for _, group in df.groupby('calc_time') if not group.empty]
        group_eval_combinations = combinations(range(len(grouped_eval_data)),2)
        results = []
        for i, j in group_eval_combinations:
            group1 = grouped_eval_data[i]
            group2 = grouped_eval_data[j]
            u_stat, p_val = stats.mannwhitneyu(group1,group2)
            results.append({
                'Time1' : i, 
                'Time2' : j,
                'u_stat' : u_stat,
                'p-val' : p_val,
                'Reject' : "True" if p_val < 0.05 else "False"
            })
            
        results_df = pd.DataFrame(results)
        
        with open(f"./{output_directory}/chess_data_analysis{input_file.rstrip('.csv').lstrip('/chess_datascore')}.txt", "w") as file:
                pd.set_option('display.max_rows', None)  # Show all rows
                pd.set_option('display.max_columns', None)  # Show all columns
                pd.set_option('display.show_dimensions',False)
                results_df = results_df.reset_index(drop=True)
                print(results_df.to_string(index=False), file=file)
      

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
    if len(sys.argv) >= 3:
        main()
    else: 
        print('Not enough arguments provided.')