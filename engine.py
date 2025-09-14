import torch
import chess
import sys
class Engine():
    def value(self, piece: str):
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
    def encode(self, fen: str):
        representation = []
        board = fen.split(" ")[0]
        ranks = board.split("/")
        for rank in ranks:
            for square in rank:
                if square.isdigit():
                    for _ in range(int(square)):
                        representation.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
                else:
                    representation.append(self.value(square))
        return representation
    def __init__(self):
        pass
    def evaluate(self, all_moves: str, fen: str):
        if fen == "startpos":
            self.board = chess.Board()
        else:
            self.board = chess.Board(fen=fen)
        all_moves = all_moves.split(" ")
        for move in all_moves:
            if move != '':
                self.board.push_uci(move)
        if self.board.is_game_over() or self.board.can_claim_draw():
            if self.board.is_game_over():
                return [[], self.board.result()]
            elif self.board.can_claim_draw():
                return [[], '1/2-1/2']
        if self.board.turn == chess.WHITE:
            color = 1
        elif self.board.turn == chess.BLACK:
            color = -1
        legal_moves = [move.uci() for move in self.board.legal_moves]
        best_moves = []
        evaluations = []
        device = torch.device("mps")
        model = torch.load('model.pth', weights_only=False).to(device)
        for move in legal_moves:
            self.board.push_uci(move)
            model.eval()
            with torch.no_grad():
                encoded_board = self.encode(self.board.fen())
                tensor = torch.tensor(encoded_board, dtype=torch.float).to(device)
                tensor = tensor.flatten()
                tensor = tensor.unsqueeze(0)
                prediction = model(tensor)
            self.board.pop()
            evaluations.append([prediction.item()*color, move])
        best_eval = -sys.maxsize
        for eval in evaluations:
            if eval[0] > best_eval:
                best_eval = eval[0]
                best_moves.clear()
                best_moves.append(eval[1])
            elif eval[0] == best_eval:
                best_moves.append(eval[1])
        return [best_moves, '*']