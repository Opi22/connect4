# core/board.py
from copy import deepcopy

ROWS = 6
COLS = 7
EMPTY = 0
PLAYER = 1
AI = 2
WINDOW = 4


class Board:
    def __init__(self):
        self.grid = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

    def copy(self):
        b = Board()
        b.grid = deepcopy(self.grid)
        return b

    def drop_piece(self, row, col, piece):
        self.grid[row][col] = piece

    def is_valid_col(self, col):
        return self.grid[0][col] == EMPTY

    def get_valid_cols(self):
        return [c for c in range(COLS) if self.is_valid_col(c)]

    def get_next_row(self, col):
        for r in range(ROWS - 1, -1, -1):
            if self.grid[r][col] == EMPTY:
                return r
        return None

    def winning_move(self, piece):
        g = self.grid

        # horizontal
        for r in range(ROWS):
            for c in range(COLS - 3):
                if all(g[r][c + i] == piece for i in range(4)):
                    return True

        # vertical
        for c in range(COLS):
            for r in range(ROWS - 3):
                if all(g[r + i][c] == piece for i in range(4)):
                    return True

        # positive diagonal
        for r in range(3, ROWS):
            for c in range(COLS - 3):
                if all(g[r - i][c + i] == piece for i in range(4)):
                    return True

        # negative diagonal
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                if all(g[r + i][c + i] == piece for i in range(4)):
                    return True

        return False

    def is_terminal(self):
        return (
            self.winning_move(PLAYER)
            or self.winning_move(AI)
            or len(self.get_valid_cols()) == 0
        )

    # ------ Heuristic evaluation ------
    def score_window(self, window, piece):
        opp = PLAYER if piece == AI else AI
        score = 0

        if window.count(piece) == 4:
            score += 1000
        elif window.count(piece) == 3 and window.count(EMPTY) == 1:
            score += 50
        elif window.count(piece) == 2 and window.count(EMPTY) == 2:
            score += 10

        if window.count(opp) == 3 and window.count(EMPTY) == 1:
            score -= 80

        return score

    def score_position(self, piece):
        score = 0
        g = self.grid

        # center column preference
        center_col = [g[r][COLS // 2] for r in range(ROWS)]
        score += center_col.count(piece) * 6

        # horizontal
        for r in range(ROWS):
            row = g[r]
            for c in range(COLS - 3):
                window = row[c:c + WINDOW]
                score += self.score_window(window, piece)

        # vertical
        for c in range(COLS):
            col = [g[r][c] for r in range(ROWS)]
            for r in range(ROWS - 3):
                window = col[r:r + WINDOW]
                score += self.score_window(window, piece)

        # positive diagonal
        for r in range(3, ROWS):
            for c in range(COLS - 3):
                window = [g[r - i][c + i] for i in range(WINDOW)]
                score += self.score_window(window, piece)

        # negative diagonal
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                window = [g[r + i][c + i] for i in range(WINDOW)]
                score += self.score_window(window, piece)

        return score
