import chess
from evaluate import evaluate


def get_legal_moves_from_board(board):
    legal_moves = board.legal_moves
    moves = []

    for m in legal_moves:
        moves.append(m)
    return moves


def get_capture_moves_from_board(board):
    capture_moves = []
    moves = get_legal_moves_from_board(board)

    for m in moves:
        if board.is_capture(m):
            capture_moves.append(m)
    return capture_moves


def get_possible_moves_from_board(board):
    capture_moves = get_capture_moves_from_board(board)
    if len(capture_moves) > 0:
        return capture_moves
    else:
        return get_legal_moves_from_board(board)


class ChessBoard:
    def __init__(self):
        self.board = chess.Board()

    def get_legal_moves(self):
        return get_legal_moves_from_board(self.board)

    def get_capture_moves(self):
        return get_capture_moves_from_board(self.board)

    def get_possible_moves(self):
        return get_possible_moves_from_board(self.board)

    def push(self, move):
        self.board.push(move)
        return self.board

    def pop(self, board=None):
        if (board != None):
            board.pop()
        else:
            self.board.pop()

    def copy(self):
        return self.board.copy()

    def parse_uci(self, string):
        self.board.parse_uci(string)
        print(string)

    # def display(self):
    #     display(self.board)

    def is_checkmate(self):
        return self.board.is_checkmate()


    def print_moves(self, moves):
        print("Possible moves")
        for m in moves:
            print(m)

    def is_valid_move(self, move):
        possible_moves = self.get_possible_moves()
        if move in possible_moves:
            return True
        else:
            return False

    def turn(self):
        return self.board.turn

    def evaluate(self):
        return evaluate(self.board, self.turn())
