from anytree import AnyNode
from chess.polyglot import zobrist_hash
import random

from evaluate import evaluate
from chessboard import get_possible_moves_from_board

count = 0


def tree(node, depth, max_depth, turn, stack):
    global count
    if depth <= max_depth and not node.board.is_stalemate() and not node.board.is_checkmate():
        possiblemoves = get_possible_moves_from_board(node.board)
        if 0 < len(possiblemoves) <= 4:
            max_depth += 1 / len(possiblemoves)
        if len(possiblemoves) >= 35:
            max_depth -= 1 / 2
        alpha = node.alpha
        beta = node.beta
        if (depth % 2) == 0:
            value = -99999
            for i in range(len(possiblemoves)):
                newboard = node.board
                newboard.push(possiblemoves[i])
                board_hash = zobrist_hash(newboard)
                if board_hash in stack:
                    newboard.pop()
                    continue
                else:
                    stack.append(board_hash)
                ndata = {"board": newboard, "move": possiblemoves[i], "alpha": alpha, "beta": beta, "value": None}
                nnode = AnyNode(**ndata)
                nnode.parent = node
                tree(nnode, depth + 1, max_depth, turn, stack)
                newboard.pop()
                stack.pop()
                value = max(nnode.value, value)
                if value >= beta:
                    break
                # if value == 10000:
                #   break
                alpha = max(value, alpha)
            node.value = value
            return node
        else:
            value = 99999
            for i in range(len(possiblemoves)):
                newboard = node.board
                newboard.push(possiblemoves[i])
                board_hash = zobrist_hash(newboard)
                if board_hash in stack:
                    newboard.pop()
                    continue
                else:
                    stack.append(board_hash)
                ndata = {"board": newboard, "move": possiblemoves[i], "alpha": alpha, "beta": beta, "value": None}
                nnode = AnyNode(**ndata)
                nnode.parent = node
                tree(nnode, depth + 1, max_depth, turn, stack)
                newboard.pop()
                stack.pop()
                value = min(value, nnode.value)
                if value <= alpha:
                    break
                # if value == -10000:
                #   break
                beta = min(value, beta)
            node.value = value
            return node
    else:
        node.value = evaluate(node.board, turn)
        count += 1
        return node



root_node = None


def get_move(root):
    global count
    global root_node
    # print("evaluate count: ", count)
    count = 0

    if root.value == 10000:
        for i in range(len(root.children)):
            if root.children[i].value == 10000:
                root_node = root.children[i]
                return root_node.move

    moves = get_possible_moves_from_board(root.board)
    stack = []
    for i in root.children:
        # print(moves[c.children.index(i)], i.value)
        # print(moves[root.children.index(i)], i)
        if i.value == root.value:
            stack.append(moves[root.children.index(i)])
    if len(stack) == 0:
        return ""
    r = random.randint(0, len(stack) - 1)
    # print(r, len(stack))
    return stack[r]


def find_move(board, depth, turn):
    global root_node
    data = {"board": board, "alpha": float('-99999'), "beta": float('99999'), "value": None}
    root = AnyNode(**data)
    tree(root, 0, int(depth), turn, [])
    if root.value == 10000:
        root_node = root

        return get_move(root), True
    return get_move(root), False


def find_checkmate():
    global root_node
    for i in range(len(root_node.children)):
        if root_node.children[i].value == 10000:
            root_node = root_node.children[i]
            # print(root_node)
            return root_node.move


def counter_checkmate(move):
    global root_node
    for i in range(len(root_node.children)):
        if root_node.children[i].move == move:
            root_node = root_node.children[i]
            # print(root_node)
            return
