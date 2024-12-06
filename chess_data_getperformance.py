import pandas as pd 
import sys 
import matplotlib.pyplot as plt

chess_data_csv_output_list = ['/chess_datascore0-1000Elo.csv', 
                       '/chess_datascore1000-1250Elo.csv',
                       '/chess_datascore1250-1500Elo.csv',
                       '/chess_datascore1500-1750Elo.csv',
                       '/chess_datascore1750-2000Elo.csv',
                       '/chess_datascore2000-2250Elo.csv',
                       '/chess_datascore2250+Elo.csv'
                       ]

chess_data_csv_input_list = ['/chess_data0-1000Elo.csv', 
                       '/chess_data1000-1250Elo.csv',
                       '/chess_data1250-1500Elo.csv',
                       '/chess_data1500-1750Elo.csv',
                       '/chess_data1750-2000Elo.csv',
                       '/chess_data2000-2250Elo.csv',
                       '/chess_data2250+Elo.csv'
                       ]


def time_to_seconds(time):
    hrs, mins, secs = map(int, time.split(':'))
    return hrs * 3600 + mins * 60 + secs

def caluclate_time(start_time, end_time):
    if(start_time == None):
        return 0
    return time_to_seconds(end_time) - time_to_seconds(start_time)

def calculate_eval(current_eval, previous_eval, turn):
    if('#' in str(current_eval) or '#' in str(previous_eval)):
        return None, turn%2
    elif(previous_eval is None and current_eval is None):
        return None     
    elif(previous_eval is None):
        return current_eval

    return float(current_eval) - float(previous_eval), turn%2

def get_game_performance(game):
    eval_score = game['Evaluations'].split(' ')
    time = game['Clocks'].split(' ')
    max = 0
    if(len(eval_score) <= len(time)) : max = len(eval_score)
    else:
        print(game) 
        max = len(time)

    dataframe = pd.DataFrame({"Eval" : eval_score[:max], 'Time' : time[:max], 'Turn' : list(range(1,max+1))})
    dataframe['Previous_Eval'] = dataframe['Eval'].shift(1)
    dataframe['Previous_Time'] = dataframe['Time'].shift(2)

    dataframe['calc_time'] = dataframe.apply(lambda x: caluclate_time(x['Previous_Time'], x['Time']), axis = 1)

    dataframe['calc_eval'] = dataframe.apply(lambda x: calculate_eval(x['Eval'],x['Previous_Eval'], x['Turn'])[0], axis = 1)
    dataframe['Player'] = dataframe.apply(lambda x: calculate_eval(x['Eval'], x['Previous_Eval'], x['Turn'])[1], axis = 1)
    dataframe.dropna(inplace=True)
    return dataframe.drop(columns=['Previous_Eval', 'Previous_Time', 'Eval', 'Time'],axis = 1)
  
def main():
    input_directory = sys.argv[1]
    output_directory = sys.argv[2]

    chess_data = pd.read_csv(input_directory + chess_data_csv_input_list[1])
    chess_data.dropna(inplace=True)
    game_performance = chess_data.apply(lambda x: get_game_performance(x), axis = 1)    
    game_performance = pd.concat(game_performance.tolist(), ignore_index = True)
    game_performance = game_performance[game_performance['calc_time'] >= 0]
    game_performance_white = game_performance[game_performance['Player'] == 1]
    game_performance_black = game_performance[game_performance['Player'] == 0]

    game_performance_white = game_performance_white.groupby('calc_time').agg({'calc_eval': 'mean'}).reset_index()
    game_performance_black = game_performance_black.groupby('calc_time').agg({'calc_eval': 'mean'}).reset_index()

    plt.figure(figsize=(14, 10))
    plt.xlabel('Clock Time (seconds)')
    plt.ylabel('Average Evaluation Score')
    plt.title('Average Evaluation Score vs. Clock Time for Different Elo Ranges (White and Black Moves)')
    plt.legend(title="Elo Range and Player")
    plt.grid(True)
    plt.plot(game_performance_black['calc_time'], game_performance_black['calc_eval'])
    plt.savefig('temp.png')
if __name__ == '__main__':
    if(len(sys.argv) >= 3):
        main()
    else: 
        print('not enough args')