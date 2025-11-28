# core/game.py
from core.board import Board, PLAYER, AI
from core.ai import AIPlayer


class Game:
    def __init__(self, depth=5):
        self.board = Board()
        self.turn = PLAYER  # player goes first
        self.ai = AIPlayer(depth)
        self.game_over = False

    def reset(self):
        self.__init__()

    def make_player_move(self, col):
        if self.game_over:
            return False

        if self.board.is_valid_col(col):
            row = self.board.get_next_row(col)
            self.board.drop_piece(row, col, PLAYER)

            if self.board.winning_move(PLAYER):
                self.game_over = True
                return "player_win"

            self.turn = AI
            return True

        return False

    def make_ai_move(self):
        if self.game_over:
            return False

        col = self.ai.get_move(self.board)
        if col is None:
            self.game_over = True
            return False

        row = self.board.get_next_row(col)
        self.board.drop_piece(row, col, AI)

        if self.board.winning_move(AI):
            self.game_over = True
            return "ai_win"

        self.turn = PLAYER
        return True
