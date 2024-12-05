import pandas as pd
import re

# Load the CSV data containing the moves and clock information
csv_file_path = "./chess_data/chess_data0-1000Elo.csv"  # Update with the actual path to your CSV file
chess_data = pd.read_csv(csv_file_path)

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

# Process each row in the CSV
all_evals = []
all_clocks = []

for index, row in chess_data.iterrows():
    evals, clocks = parse_clk_column(row['Clk'])
    all_evals.append(evals)
    all_clocks.append(clocks)

# Add the extracted evaluations and clock times as new columns
chess_data['Evaluations'] = all_evals
chess_data['Clocks'] = all_clocks

# Remove the original Clk column
chess_data = chess_data.drop(columns=['Clk'])

# Save the parsed data to a new CSV file
chess_data.to_csv("parsed_chess_data.csv", index=False)

print("Parsing completed successfully and saved to 'parsed_chess_data.csv'.")
