import pandas as pd
import os
import sys
import re
import matplotlib.pyplot as plt
import numpy as np



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
        'blue', 'green', 'red', 'purple', 'orange', 'brown', 'pink'
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
                
        # Plot scatter plot for White players
        plt.figure(figsize=(10, 5))
        white_data = df[df['Player'] == 1]
        plt.scatter(white_data['calc_time'], white_data['Calc_Eval'], c=colors[i], edgecolor='black', marker='o', label=f'White (o) {csv_file}')
                
        plt.xlabel('Calculation Time')
        plt.ylabel('Calculation Evaluation')
        plt.title(f'Calculation Evaluation vs. Calculation Time for White Players ({csv_file})')
        plt.legend()
        #plt.show()
        plt.savefig(f'white_players_{csv_file.replace(".csv", "")}.png')
        plt.close()
        
        # Plot scatter plot for Black players
        plt.figure(figsize=(10, 5))
        black_data = df[df['Player'] == 0]
        plt.scatter(black_data['calc_time'], -black_data['Calc_Eval'], c=colors[i], edgecolor='black', marker='^', label=f'Black (x) {csv_file}')
                
        plt.xlabel('Calculation Time')
        plt.ylabel('Calculation Evaluation')
        plt.title(f'Calculation Evaluation vs. Calculation Time for Black Players ({csv_file})')
        plt.legend()
        #plt.show()
        plt.savefig(f'black_players_{csv_file.replace(".csv", "")}.png')
        plt.close()



if __name__ == '__main__':
    if len(sys.argv) >= 2:
        main()
    else: 
        print('Not enough arguments provided.')
