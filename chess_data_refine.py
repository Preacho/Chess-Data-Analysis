import pandas as pd
import sys 
import re

chess_data_csv_list = ['/chess_data0-1000Elo.csv', 
                       '/chess_data1000-1250Elo.csv',
                       '/chess_data1250-1500Elo.csv',
                       '/chess_data1500-1750Elo.csv',
                       '/chess_data1750-2000Elo.csv',
                       '/chess_data2000-2250Elo.csv',
                       '/chess_data2250+Elo.csv'
                       ]

# Function to extract evals and clock times from the Clk column
def parse_clk_column(clk_data):
    evals = []
    clocks = []

    # Use regex to extract evaluation scores and clock times
    eval_matches = re.findall(r'\[%eval ([#\-\d\.]+)\]', clk_data)
    clock_matches = re.findall(r'\[%clk (\d+:\d{2}:\d{2})\]', clk_data)

    # Append matches to the lists
    for eval_match in eval_matches:
        evals.append(eval_match)

    for clock_match in clock_matches:
        clocks.append(clock_match)

    return evals, clocks

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

        # Process each row in the CSV
        all_evals = []
        all_clocks = []

        for index, row in dataframe_filter.iterrows():
            evals, clocks = parse_clk_column(row['Clk'])

            # Convert list to comma-separated string to remove quotes
            all_evals.append(' '.join(map(str, evals)))
            all_clocks.append(' '.join(map(str, clocks)))

        # Add the extracted evaluations and clock times as new columns
        dataframe_filter['Evaluations'] = all_evals
        dataframe_filter['Clocks'] = all_clocks

        # Remove the original 'Clk' column
        dataframe_filter = dataframe_filter.drop(columns=['Clk'])
        
        dataframe_filter.to_csv(input_file + strings, index = False,  encoding="utf-8")
        print(strings + " filtered!!")
    return


if __name__ == '__main__':
    if(len(sys.argv) >= 2):
        main()
    else:
        print("Not Enough Args")