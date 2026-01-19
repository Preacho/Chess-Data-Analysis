#Chess Data Analysis
Our code aims to answer the question: "Looking at different skill groups, how does time affect a player’s performance during a match?"

# Required Libraries to Install:

- pip install chess
- pip install python-chess
- pip install zstandard
- pip install pandas
- pip install numpy 
- pip install matplotlib
- pip install scipy

# Files and Scripts:
Explain the purpose of each file:
- **chess_data_extraction.py:** Extracts features like moves, Elo, and evaluations from raw Lichess data.
- **chess_data_refine.py:** Cleans data, extracting evaluation scores and clock times, and prepares datasets for analysis.
- **chess_data_getperformance.py:** Calculates player improvement metrics, such as changes in evaluation scores.
- **move_evaluations.py:** (Optional) Evaluates individual chess moves using the Stockfish engine.
- **plot_avg_evals.py:** Generates scatter plots to visualize the relationship between calculation time and evaluation scores.
- **chess_data_decision_time_mann_whitney.py:** Performs Mann-Whitney U-tests to analyze decision time's impact on performance.
- **chess_data_indepthtime_mann_whitney.py:** Provides an in-depth analysis by iterating through all possible decision time groups.

# Folders: 
- **chess_data_images:** Contains pictures of the scatter plots for the different Elo ranges. 
- **chess_data_score:** Contains the data of the player improvement metrics that were used for analysis. 
- **chess_data_anaylsis:** Contains the output data from the chess_data_indepthtime_mann_whitney.py file. This is used for the analysis in the report.

# Execution order:
- Download a dataset of games from https://database.lichess.org/

- Run chess_data_extraction.py which will save the csv files to chess_data folder:
  - python chess_data_extraction.py downloaded_datafilename.pgn.zst
  - The extracted dataset will be outputted into a folder called chess_data
  - Takes a long time

- Run chess_data_refine.py
  - (contains 1 argument for an input folder. Use chess_data folder)
  - python chess_data_refine.py chess_data

- Run chess_data_getperformance.py 
  - (contains arguments of an input folder (chess_data) and output folder)
  - Python chess_data_getperformance.py chess_data output_folder_name

- Run plot_avg_evals.py 
  - (contains 1 argument input the output_folder_name created from chess_data_getperformance.py)
  - python plot_avg_evals.py output_folder_name

- Run chess_data_decision_time_mann_whitney.py
  - (contains 1 argument input the output_folder_name created from chess_data_getperformance.py)
  - python chess_data_decision_time_mann_whitney.py output_folder_name

- Run chess_data_indepthtime_mann_whitney.py
  - (contains 1 argument input the output_folder_name created from chess_data_getperformance.py)
  - python chess_data_indepthtime_mann_whitney.py output_folder_name

# Data Source:
- Lichess Open Database: https://database.lichess.org/
  - Datasets included over 45 million games recorded from January 2020, including clock and Stockfish evaluation data.
