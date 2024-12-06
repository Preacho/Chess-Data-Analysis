import chess 
import chess.engine
import pandas as pd

# Load the Stockfish engine
engine_path = "./stockfish/stockfish-windows-x86-64-avx2.exe"

engine = chess.engine.SimpleEngine.popen_uci(engine_path)

# Load the CSV data containing the moves
csv_file_path = "./chess_data/chess_data0-1000Elo.csv"  # Update with the actual path to your CSV
chess_data = pd.read_csv(csv_file_path)

# Function to classify the quality of a move
def get_evaluation_after_move(fen, move):
    board = chess.Board(fen)
    move_obj = chess.Move.from_uci(move)

    # Make the move
    board.push(move_obj)

    # Evaluate the position after the move
    info_after = engine.analyse(board, chess.engine.Limit(time=0.1))
    eval_after = info_after["score"].white().score()

    return eval_after

# Process each row in the CSV
results = []
for index, row in chess_data.iterrows():
    board = chess.Board()  # Start with the initial chess board
    moves = row["Moves"].split()  # Extract the moves from the CSV column
    for move in moves:
        try:
            eval_after = get_evaluation_after_move(board.fen(), move)
        except:
            eval_after = None  # Handle invalid moves
        results.append({"GameID": index, "Move": move, "EvalAfter": eval_after})
        board.push(chess.Move.from_uci(move))  # Update the board state

# Convert to DataFrame and save the classifications
classified_moves = pd.DataFrame(results)
classified_moves.to_csv("classified_moves.csv", index=False)

# Close Stockfish
engine.quit()