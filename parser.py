import chess
import chess.pgn
import sys
input = []
output = []
def value(piece: str):
    # Structure = pnbrqkPNBRQK
    if piece == 'p':
        return [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    elif piece == 'n':
        return [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    elif piece == 'b':
        return [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    elif piece == 'r':
        return [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
    elif piece == 'q':
        return [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
    elif piece == 'k':
        return [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
    elif piece == 'P':
        return [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
    elif piece == 'N':
        return [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
    elif piece == 'B':
        return [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
    elif piece == 'R':
        return [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
    elif piece == 'Q':
        return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
    elif piece == 'K':
        return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
def encode(fen: str):
    representation = []
    board = fen.split(" ")[0]
    ranks = board.split("/")
    for rank in ranks:
        for square in rank:
            if square.isdigit():
                for _ in range(int(square)):
                    representation.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            else:
                representation.append(value(square))
    return representation
file = open(sys.argv[1])
games = 0
while True:
    game = chess.pgn.read_game(file)
    if game is None:
        break
    pgn_result = game.headers['Result']
    if pgn_result == "1-0":
        result = 1
    elif pgn_result == "1/2-1/2":
        result = 0
    elif pgn_result == "0-1":
        result = -1
    board = chess.Board()
    for move in game.mainline_moves():
        board.push(move)
        input.append(encode(board.fen()))
        output.append([result])
    games += 1
    print(f"Game {games} completed")
chunk_size = 100
input = [input[chunk:chunk+chunk_size] for chunk in range(0, len(input), chunk_size)]
output = [output[chunk:chunk+chunk_size] for chunk in range(0, len(output), chunk_size)]
for count, chunk in enumerate(input):
    file = open(f"{sys.argv[2]}/{count}.txt", "w")
    file.write(str(chunk) + '\n')
    file.write(str(output[count]))
    file.close()