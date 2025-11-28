# core/ai.py
import math
import random
from core.board import Board, PLAYER, AI


class AIPlayer:
    def __init__(self, depth=5):
        self.depth = depth

    def minimax(self, board, depth, alpha, beta, maximizing):
        valid_cols = board.get_valid_cols()
        terminal = board.is_terminal()

        if depth == 0 or terminal:
            if terminal:
                if board.winning_move(AI):
                    return None, 10**9
                elif board.winning_move(PLAYER):
                    return None, -10**9
                else:
                    return None, 0
            else:
                return None, board.score_position(AI)

        if maximizing:
            best_val = -math.inf
            best_col = random.choice(valid_cols)

            for col in valid_cols:
                row = board.get_next_row(col)
                new_board = board.copy()
                new_board.drop_piece(row, col, AI)

                _, score = self.minimax(new_board, depth - 1, alpha, beta, False)

                if score > best_val:
                    best_val = score
                    best_col = col

                alpha = max(alpha, best_val)
                if alpha >= beta:
                    break

            return best_col, best_val

        else:
            best_val = math.inf
            best_col = random.choice(valid_cols)

            for col in valid_cols:
                row = board.get_next_row(col)
                new_board = board.copy()
                new_board.drop_piece(row, col, PLAYER)

                _, score = self.minimax(new_board, depth - 1, alpha, beta, True)

                if score < best_val:
                    best_val = score
                    best_col = col

                beta = min(beta, best_val)
                if alpha >= beta:
                    break

            return best_col, best_val

    def get_move(self, board):
        col, _ = self.minimax(board, self.depth, -math.inf, math.inf, True)
        return col
