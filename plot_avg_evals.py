import pandas as pd
import os
import sys
import re
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress



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
        white_data = df[df['Player'] == 1]
        black_data = df[df['Player'] == 0]

        plt.scatter(white_data['calc_time'], white_data['Calc_Eval'], c=colors[i], edgecolor='black', marker='o', label=f'Player (o) {csv_file}')
        plt.scatter(black_data['calc_time'], -black_data['Calc_Eval'], c=colors[i], edgecolor='black', marker='o')

        # Perform linear regression for players
        fit = linregress(white_data['calc_time'], white_data['Calc_Eval'])
        regression_line = fit.slope * white_data['calc_time'] + fit.intercept
        plt.plot(white_data['calc_time'], regression_line, color='red', linestyle='--', label=f'Regression Line')
                
        plt.xlabel('Calculation Time')
        plt.ylabel('Calculation Evaluation')
        plt.title(f'Calculation Evaluation vs. Calculation Time for ({csv_file})')
        plt.legend()
        #plt.show()
        plt.savefig(f'players_{csv_file.replace(".csv", "")}.png')
        plt.close()
        

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        main()
    else: 
        print('Not enough arguments provided.')
