import pandas as pd 
import numpy as np
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
    return   (hrs * 3600 + mins * 60 + secs) 

def caluclate_time(start_time, end_time):
    if(start_time == None):
        return 0
    return (time_to_seconds(end_time) - time_to_seconds(start_time)) *-1

def determine_improvement(calc_eval, turn):
    if(calc_eval == None):
        return None 
    if(turn%2 == 0):
        if(float(calc_eval) * -1 > 0): return 1.0 
        return 0.0
    
    if(float(calc_eval) > 0): return 1.0 
    return 0.0

def calculate_evaluation(current_eval, previous_eval, turn):
    if('#' in str(current_eval) or '#' in str(previous_eval)):
        return None, turn%2
    elif(previous_eval is None and current_eval is None):
        return None, turn%2
    elif(previous_eval is None):
        return float(current_eval), turn%2

    return float(current_eval) - float(previous_eval), turn%2

def get_game_performance(game):
    eval_score = game['Evaluations'].split(' ')
    time = game['Clocks'].split(' ')
    max = 0
    if(len(eval_score) <= len(time)) : max = len(eval_score)
    else: max = len(time)

    dataframe = pd.DataFrame({"Eval" : eval_score[:max], 'Time' : time[:max], 'Turn' : list(range(1,max+1))})
    dataframe['Previous_Eval'] = dataframe['Eval'].shift(1)
    dataframe['Previous_Time'] = dataframe['Time'].shift(2)
    dataframe['calc_time'] = dataframe.apply(lambda x: caluclate_time(x['Previous_Time'], x['Time']), axis = 1)

    dataframe['Player'] = dataframe.apply(lambda x: calculate_evaluation(x['Eval'], x['Previous_Eval'], x['Turn'])[1], axis = 1)
    dataframe['Calc_Eval'] = dataframe.apply(lambda x: calculate_evaluation(x['Eval'], x['Previous_Eval'], x['Turn'])[0], axis = 1)
    dataframe['Improvement'] = dataframe.apply(lambda x: determine_improvement(x['Calc_Eval'], x['Turn']), axis = 1)
    
    dataframe.dropna(inplace=True)
    return dataframe.drop(columns=['Previous_Eval', 'Previous_Time', 'Eval', 'Time'],axis = 1)
  
def main():
    input_directory = sys.argv[1]
    output_directory = sys.argv[2]

    chess_data = pd.read_csv(input_directory + chess_data_csv_input_list[6])
    chess_data.dropna(inplace=True)
    game_performance = chess_data.apply(lambda x: get_game_performance(x), axis = 1)    
    game_performance = pd.concat(game_performance.tolist(), ignore_index = True)
    
    game_performance = game_performance[(game_performance['calc_time'] >= 0)  & (game_performance['calc_time'] <= 300)]
    print(game_performance)
    
    game_performance_white = game_performance[game_performance['Player'] == 1]
    game_performance_black = game_performance[game_performance['Player'] == 0]

    game_performance_white = game_performance_white.groupby('calc_time').agg({'Improvement': 'mean'}).reset_index()
    
    #Setting Bins and Labels. Mess with it
    bins = [0,5,10,15,20,25,30,35,40,45,50,55,60,
            90,120,150,180,210,240,270,300]
    
    labels = ['0-5','5-10','10-15','15-20','20-25','25-30','30-35','35-40','40-45','45-50','50-55','55-60',
              '60-90','90-120', '120-150','150-180','180-210','210-240','240-270','270-300']
    
    
    game_performance_white['time_group'] = pd.cut(game_performance_white['calc_time'], bins = bins, labels = labels, right = False)
    game_performance_white = game_performance_white.groupby('time_group').agg({'Improvement' : 'mean'}).reset_index()
    
    
    plt.figure(figsize=(14, 10))
    plt.xlabel('Clock Time (seconds)')
    plt.ylabel('Relative Number of Improvements')
    plt.title('Number of Imporvements vs Clock Time')
    plt.grid(True)
    plt.plot(game_performance_white['time_group'], game_performance_white['Improvement'])
    plt.savefig('temp.png')
    
    game_performance.to_csv(output_directory + chess_data_csv_output_list[6], index = False,  encoding="utf-8")
    
    
if __name__ == '__main__':
    if(len(sys.argv) >= 3):
        main()
    else: 
        print('not enough args')