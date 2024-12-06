import pandas as pd
import os
import sys
import re
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress
import statsmodels.api as sm



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
    
    colors = [
        'blue', 'green', 'yellow', 'purple', 'orange', 'brown', 'pink'
    ]
    
    # Combine all data into a single DataFrame
    data_frames = []
    for csv_file in chess_data_csv_list:
        file_path = os.path.join(input_directory, csv_file)
        df = pd.read_csv(file_path)
        data_frames.append(df)
        
    # Plot separate graphs for each Elo range
    for i, csv_file in enumerate(chess_data_csv_list):
        file_path = os.path.join(input_directory, csv_file)
        df = pd.read_csv(file_path)
        df['Calc_Eval'] = df.apply(lambda x: x['Calc_Eval'].astype(float) * -1.0 if x['Player'] == 0.0 else x['Calc_Eval'].astype(float), axis = 1)
        
        # Plot scatter plot for White players
        plt.figure(figsize=(10, 5))
        great_data = df[(df['Calc_Eval'] >= 0) & (df['calc_time'] <= 60)]
        plt.scatter(great_data['calc_time'], great_data['Calc_Eval'], c=colors[i], edgecolor='black', marker='o', label=f'White (o) {csv_file}')

        lowess = sm.nonparametric.lowess
        relative_great_data = great_data.groupby('calc_time').agg({'Calc_Eval': 'mean'}).reset_index()
        loess_smoothed_great = lowess(relative_great_data['calc_time'], relative_great_data['Calc_Eval'], frac = 0.8, it= 3)
        print(loess_smoothed_great[:,1])
        plt.plot(relative_great_data['calc_time'], loess_smoothed_great[:,1], '-r') 
            
            
        plt.xlabel('Calculation Time')
        plt.ylabel('Calculation Evaluation')
        plt.title(f'Calculation Evaluation vs. Calculation Time for Players ({csv_file})')
        plt.legend()
        #plt.show()
        plt.savefig(f'chess_data_img/improvement_players_{csv_file.replace(".csv", "")}.png')
        plt.close()
        
        # Plot scatter plot for Black players
        plt.figure(figsize=(10, 5))
        mistake_data = df[df['Calc_Eval'] < 0]
        plt.scatter(mistake_data['calc_time'], mistake_data['Calc_Eval'], c=colors[i], edgecolor='black', marker='^', label=f'Black (x) {csv_file}')


        plt.xlabel('Calculation Time')
        plt.ylabel('Calculation Evaluation')
        plt.title(f'Calculation Evaluation vs. Calculation Time for Black Players ({csv_file})')
        plt.legend()
        #plt.show()
        plt.savefig(f'chess_data_img/mistake_players_{csv_file.replace(".csv", "")}.png')
        plt.close()
        



if __name__ == '__main__':
    if len(sys.argv) >= 2:
        main()
    else: 
        print('Not enough arguments provided.')
