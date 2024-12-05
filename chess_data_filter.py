import pandas as pd
import sys 

chess_data_csv_list = ['/chess_data0-1000Elo.csv', 
                       '/chess_data1000-1250Elo.csv',
                       '/chess_data1250-1500Elo.csv',
                       '/chess_data1500-1750Elo.csv',
                       '/chess_data1750-2000Elo.csv',
                       '/chess_data2000-2250Elo.csv',
                       '/chess_data2250+Elo.csv'
                       ]

def main():
    #Input is Folder Directory of the csv files
    
    input_file = sys.argv[1]
    for strings in chess_data_csv_list:
        dataframe = pd.read_csv(input_file + strings)
        #Remvoe All question marks
        dataframe_filter = dataframe[dataframe['Opening'] != "?"]
        #Remove All appended Headers
        dataframe_filter = dataframe_filter[dataframe_filter['Opening'] != 'Opening']
        
        #Include Only the '%eval
        dataframe_filter = dataframe_filter[dataframe_filter['Clk'].str.contains('%eval', na=False)]
        
        dataframe_filter.to_csv(input_file + strings, index = False,  encoding="utf-8")
        print(strings + " filtered!!")
    return


if __name__ == '__main__':
    if(len(sys.argv) >= 2):
        main()
    else:
        print("Not Enough Args")