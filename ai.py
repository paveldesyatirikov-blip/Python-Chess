import copy
import random
from constants import PIECE_VALUES

def evaluate_board(board):
    score = 0
    for r in range(8):
        for c in range(8):
            piece = board.grid[r][c]
            if piece:
                val = PIECE_VALUES[piece.name]
                # Bonus for controlling the center
                if 2 <= r <= 5 and 2 <= c <= 5:
                    val += 2
                score += val if piece.color == 'black' else -val
    return score

def get_all_moves(board, color):
    all_moves = []
    for r in range(8):
        for c in range(8):
            piece = board.grid[r][c]
            if piece and piece.color == color:
                for move in board.get_legal_moves(piece):
                    all_moves.append((piece, move))
    return all_moves

def minimax(board, depth, alpha, beta, maximizing):
    status = board.get_game_status()
    if depth == 0 or status != "PLAYING":
        return evaluate_board(board), None

    color = 'black' if maximizing else 'white'
    moves = get_all_moves(board, color)
    random.shuffle(moves)
    best_move = None

    if maximizing:
        max_eval = -float('inf')
        for piece, move in moves:
            temp_board = copy.deepcopy(board)
            temp_piece = temp_board.grid[piece.row][piece.col]
            temp_board.make_move(temp_piece, move[0], move[1])
            eval_score, _ = minimax(temp_board, depth - 1, alpha, beta, False)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = (piece, move)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for piece, move in moves:
            temp_board = copy.deepcopy(board)
            temp_piece = temp_board.grid[piece.row][piece.col]
            temp_board.make_move(temp_piece, move[0], move[1])
            eval_score, _ = minimax(temp_board, depth - 1, alpha, beta, True)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = (piece, move)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move