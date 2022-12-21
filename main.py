import chess
import sys
import random

from chessboard import ChessBoard, get_possible_moves_from_board
from tree import find_checkmate, find_move, counter_checkmate


def random_select(board):
    moves = get_possible_moves_from_board(board)
    ind = random.randint(0, len(moves)-1)
    return moves[ind]


def main(our_turn):
    chess_board = ChessBoard()
    # my_turn = chess.WHITE
    move_count = 0
    is_check = [None, None]
    depth = 4
    while not chess_board.is_checkmate():
        if chess_board.board.is_fifty_moves():
            # print("fifty move")
            break
        if chess_board.board.is_stalemate():
            break
        # chess_board.print_moves(chess_board.get_possible_moves())
        # print(chess_board.board)
        # chess_board.display()
        turn = chess_board.turn()
        # print(chess_board.evaluate())

        if turn == our_turn:
            if is_check[int(turn)]:
                next_move = find_checkmate()
            else:
                next_move, is_check[int(turn)] = find_move(chess_board.copy(), depth, turn)
                # print("white check:", is_check[int(turn)])
            if is_check[int(not turn)]:
                counter_checkmate(next_move)
            print(next_move)
        else:
            move = input()
            try:
                next_move = chess.Move.from_uci(move)
            except Exception:
                print("Not a valid move")
                continue
            # next_move = random_select(chess_board.board)
            # print(next_move)
            if is_check[int(not turn)]:
                counter_checkmate(next_move)
        if chess_board.is_valid_move(next_move):
            chess_board.push(next_move)
        else:
            print("Not a legal move, or not a capture move, please enter again")
            continue
        move_count += 1
        if move_count >= 15:
            depth = 3.5
    # print(chess_board.board, chess_board.turn(), our_turn, chess_board.turn() == our_turn)
    if chess_board.board.is_fifty_moves() or chess_board.board.is_stalemate():
        print("1/2-1/2")
    elif chess_board.turn() == our_turn:
        print("0-1")
    else:
        print("1-0")


if __name__ == "__main__":
    # print(sys.argv)
    bot_turn = sys.argv[1]
    if bot_turn == "white":
        bot = chess.WHITE
    elif bot_turn == "black":
        bot = chess.BLACK
    else:
        bot = chess.WHITE
    # print(bot)
    main(bot)


