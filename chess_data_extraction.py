import zstandard
import chess.pgn
import pandas as pd

from io import TextIOWrapper


#Change input file to current input file

input_file = "lichess_db_standard_rated_2020-01.pgn.zst"


def get_game_data(chess_data):

    return{

        "Event": chess_data.headers.get("Event", ""),
        "Result": chess_data.headers.get("Result", ""),
        "Opening": chess_data.headers.get("Opening", ""),
        "ECO" : chess_data.headers.get("ECO", ""),
        "WhiteElo" : chess_data.headers.get("WhiteElo",""),
        "BlackElo" : chess_data.headers.get("BlackElo",""),
        "Moves": " ".join(str(move) for move in chess_data.mainline_moves()),

    }

def main():

    game_data_list = []
    list_size = 0
    add_count = 0
    with open(input_file, "rb") as compressed_file:

    # Decompress the file

        dctx = zstandard.ZstdDecompressor()
        with dctx.stream_reader(compressed_file) as reader:

            # Parse the PGN data
            text_stream = TextIOWrapper(reader, encoding="utf-8")
            pgn = chess.pgn.read_game(text_stream)
            

            # Iterate through games in the PGN file
            while pgn is not None:

                # Extract game data and append to the list
                game_data = get_game_data(pgn)
                game_data_list.append(game_data)
                
                # Read the next game
                pgn = chess.pgn.read_game(text_stream)
                
                #Check size of the list. If it has grown too big append it onto the csvs
                list_size += 1 
                if(list_size == 10000):
                    chess_dataframe = pd.DataFrame(game_data_list)
                    
                    #Break Dataframe up into different brackets
                    
                    chess_bracket1elo = chess_dataframe[
                        (chess_dataframe['WhiteElo'].astype(int) + chess_dataframe['BlackElo'].astype(int)) / 2 < 1000
                    ]

                    # Elo 1000-1250
                    chess_bracket2elo = chess_dataframe[
                        ((chess_dataframe['WhiteElo'].astype(int) + chess_dataframe['BlackElo'].astype(int)) / 2 >=1000) &
                        ((chess_dataframe['WhiteElo'].astype(int) + chess_dataframe['BlackElo'].astype(int)) / 2 < 1250)
                    ]

                    # Elo 1250-1500
                    chess_bracket3elo = chess_dataframe[
                        ((chess_dataframe['WhiteElo'].astype(int) + chess_dataframe['BlackElo'].astype(int)) / 2 >= 1250) &
                        ((chess_dataframe['WhiteElo'].astype(int) + chess_dataframe['BlackElo'].astype(int)) / 2 < 1500)
                    ]

                    # Elo 1500-1750
                    chess_bracket4elo = chess_dataframe[
                        ((chess_dataframe['WhiteElo'].astype(int) + chess_dataframe['BlackElo'].astype(int)) / 2 >= 1500) &
                        ((chess_dataframe['WhiteElo'].astype(int) + chess_dataframe['BlackElo'].astype(int)) / 2 < 1750)
                    ]
                    
                    # Elo 1750-2000
                    chess_bracket5elo = chess_dataframe[
                        ((chess_dataframe['WhiteElo'].astype(int) + chess_dataframe['BlackElo'].astype(int)) / 2 >= 1750) &
                        ((chess_dataframe['WhiteElo'].astype(int) + chess_dataframe['BlackElo'].astype(int)) / 2 < 2000)
                    ]
                    # Elo 2000-2250
                    chess_bracket6elo = chess_dataframe[
                        ((chess_dataframe['WhiteElo'].astype(int) + chess_dataframe['BlackElo'].astype(int)) / 2 >= 2000) &
                        ((chess_dataframe['WhiteElo'].astype(int) + chess_dataframe['BlackElo'].astype(int)) / 2 < 2250)
                    ]
                    
                    #Elo 2250+
                    chess_bracket7elo = chess_dataframe[
                        ((chess_dataframe['WhiteElo'].astype(int) + chess_dataframe['BlackElo'].astype(int)) / 2 > 2250)
                    ]
                    
                    
                    chess_bracket1elo.to_csv('chess_data0-1000Elo.csv',mode = 'a', index=False, encoding="utf-8")
                    chess_bracket2elo.to_csv('chess_data1000-1250Elo.csv',mode = 'a', index=False, encoding="utf-8")
                    chess_bracket3elo.to_csv('chess_data1250-1500Elo.csv',mode = 'a', index=False, encoding="utf-8")
                    chess_bracket4elo.to_csv('chess_data1500-1750Elo.csv',mode = 'a', index=False, encoding="utf-8")
                    chess_bracket5elo.to_csv('chess_data1750-2000Elo.csv',mode='a',index=False, encoding="utf-8")
                    chess_bracket6elo.to_csv('chess_data2000-2250Elo.csv',mode = 'a', index=False, encoding="utf-8")
                    chess_bracket7elo.to_csv('chess_data2250+Elo.csv',mode='a',index=False, encoding="utf-8")
                    list_size = 0
                    game_data_list = []
                    add_count += 1
                if(add_count == 300) : break


    # Create a DataFrame from the extracted data

    if(list_size != 0):
        df = pd.DataFrame(game_data_list)
        df.to_csv('chess_data.csv',mode = 'a', index=False, encoding="utf-8")


if __name__ == '__main__':
    main()