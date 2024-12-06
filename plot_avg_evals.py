import pandas as pd
import os
import sys
import re
import matplotlib.pyplot as plt
import numpy as np

# List of filtered CSV files and their corresponding Elo ranges
filtered_chess_data_csv_list = [
    ('chess_data/chess_data0-1000Elo.csv', '0-1000 Elo'),
    ('chess_data/chess_data1000-1250Elo.csv', '1000-1250 Elo'),
    ('chess_data/chess_data1250-1500Elo.csv', '1250-1500 Elo'),
    ('chess_data/chess_data1500-1750Elo.csv', '1500-1750 Elo'),
    ('chess_data/chess_data1750-2000Elo.csv', '1750-2000 Elo'),
    ('chess_data/chess_data2000-2250Elo.csv', '2000-2250 Elo'),
    ('chess_data/chess_data2250+Elo.csv', '2250+ Elo')
]

# Function to convert clock times to seconds
def clock_time_to_seconds(clock_time):
    # Clock time format is hh:mm:ss
    time_parts = list(map(int, clock_time.split(':')))
    return time_parts[0] * 3600 + time_parts[1] * 60 + time_parts[2]

# Function to calculate average scores for each file
def calculate_average_scores():
    all_data = {
        'White': {},
        'Black': {}
    }

    # Initialize dictionary to hold data for each Elo range
    for _, elo_label in filtered_chess_data_csv_list:
        all_data['White'][elo_label] = []
        all_data['Black'][elo_label] = []

    # Read each filtered CSV file
    for csv_file, elo_label in filtered_chess_data_csv_list:
        dataframe = pd.read_csv(csv_file)

        # Convert 'Evaluations' and 'Clocks' columns to lists of floats and integers
        for index, row in dataframe.iterrows():
            if isinstance(row['Evaluations'], str) and isinstance(row['Clocks'], str):
                # Split the evaluations and clocks by whitespace
                evals = [float(x) if not x.startswith('#') else np.nan for x in row['Evaluations'].split()]
                clocks = [clock_time_to_seconds(x) for x in row['Clocks'].split()]

                # Separate evaluations and clocks for White and Black moves
                white_evals = evals[::2]
                black_evals = evals[1::2]
                white_clocks = clocks[::2]
                black_clocks = clocks[1::2]

                # Append the clock time and evaluation score to the all_data dictionary for White and Black
                '''for eval_score, clock_time in zip(white_evals, white_clocks):
                    if not np.isnan(eval_score):  # Ignore mate indications like "#-4"
                        all_data['White'][elo_label].append((clock_time, eval_score))

                for eval_score, clock_time in zip(black_evals, black_clocks):
                    if not np.isnan(eval_score):  # Ignore mate indications like "#-4"
                        all_data['Black'][elo_label].append((clock_time, eval_score))'''
                
                # Calculate evaluation differences and time taken for each White move
                for i in range(min(len(white_evals), len(black_evals))):
                    if i < len(white_clocks):
                        eval_diff = white_evals[i] - black_evals[i]  # Evaluation change from Black's move to White's move
                        time_taken = white_clocks[i] 
                        all_data['White'][elo_label].append((time_taken, eval_diff))

                # Calculate evaluation differences and time taken for each Black move
                for i in range(min(len(black_evals), len(white_evals))):
                    if i < len(black_clocks):
                        eval_diff = black_evals[i] - white_evals[i]  # Evaluation change from White's move to Black's move
                        time_taken = black_clocks[i]
                        all_data['Black'][elo_label].append((time_taken, eval_diff))

    return all_data

# Create scatter plot
def plot_average_scores(all_data):
    plt.figure(figsize=(14, 10))

    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

    # Plot each Elo range with different colors for White and Black moves
    for i, (elo_label, color) in enumerate(zip(all_data['White'].keys(), colors)):
        if all_data['White'][elo_label]:  # Ensure there's data to plot for White
            white_data_df = pd.DataFrame(all_data['White'][elo_label], columns=['ClockTime', 'EvalScore'])
            avg_white_eval_per_time = white_data_df.groupby('ClockTime').mean().reset_index()

            plt.scatter(avg_white_eval_per_time['ClockTime'], avg_white_eval_per_time['EvalScore'],
                        alpha=0.5, label=f'White - {elo_label}', color=color, marker='o')

        if all_data['Black'][elo_label]:  # Ensure there's data to plot for Black
            black_data_df = pd.DataFrame(all_data['Black'][elo_label], columns=['ClockTime', 'EvalScore'])
            avg_black_eval_per_time = black_data_df.groupby('ClockTime').mean().reset_index()

            plt.scatter(avg_black_eval_per_time['ClockTime'], avg_black_eval_per_time['EvalScore'],
                        alpha=0.5, label=f'Black - {elo_label}', color=color, marker='x')

    plt.xlabel('Clock Time (seconds)')
    plt.ylabel('Average Evaluation Score')
    plt.title('Average Evaluation Score vs. Clock Time for Different Elo Ranges (White and Black Moves)')
    plt.legend(title="Elo Range and Player")
    plt.grid(True)
    #plt.show()
    plt.savefig('temp.png')

'''def main():
    # Calculate average evaluation scores for different lengths of time
    all_data = calculate_average_scores()

    # Create scatter plot
    plot_average_scores(all_data)'''

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
