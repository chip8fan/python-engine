import engine
import secrets
import os
import chess
import sys
if os.path.isfile("model.pth") == False:
    import torch
    from torch import nn
    input_layers = 768
    hidden_layers = 1
    output_layers = 1
    model = nn.Sequential(
        nn.Linear(input_layers, hidden_layers),
        nn.LeakyReLU(),
        nn.Linear(hidden_layers, output_layers)
    )
    torch.save(model, 'model.pth')
chess_engine = engine.Engine()
moves_list = ""
uci_moves_list = ""
board = chess.Board()
move_count = 1
while True:
    moves = chess_engine.evaluate(uci_moves_list, 'startpos')
    if moves[1] != '*':
        break
    random_move = moves[0][secrets.randbelow(len(moves[0]))]
    random_move_object = chess.Move.from_uci(random_move)
    uci_moves_list = uci_moves_list + random_move + " "
    san_move = board.san(random_move_object)
    board.push(random_move_object)
    if uci_moves_list.count(" ")%2 == 0:
        moves_list = f"{moves_list}{san_move} "
        move_count += 1
    elif uci_moves_list.count(" ")%2 == 1:
        moves_list = f"{moves_list}{move_count}. {san_move} "
count = 0
while True:
    if os.path.isfile(f"{sys.argv[1]}/{count}.pgn") == False:
        break
    count += 1
file = open(f"{sys.argv[1]}/{count}.pgn", "w")
file.write(f"[Result \"{moves[1]}\"]\n")
file.write(moves_list)
file.close()