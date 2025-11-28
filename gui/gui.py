# gui/gui.py
import pygame
from core.board import ROWS, COLS, PLAYER, AI
from core.game import Game

BLUE = (12, 69, 173)
BLACK = (0, 0, 0)
RED = (220, 50, 50)
YELLOW = (240, 220, 60)
WHITE = (255, 255, 255)


class GUI:
    def __init__(self, depth=5):
        pygame.init()

        self.square = 100
        self.width = COLS * self.square
        self.height = (ROWS + 1) * self.square
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Connect 4 — OOP Minimax AI")

        self.font = pygame.font.SysFont("monospace", 45)
        self.game = Game(depth)

    def draw_board(self):
        board = self.game.board.grid

        for c in range(COLS):
            for r in range(ROWS):
                pygame.draw.rect(
                    self.screen,
                    BLUE,
                    (c * self.square, r * self.square + self.square, self.square, self.square)
                )
                pygame.draw.circle(
                    self.screen,
                    BLACK,
                    (
                        int(c * self.square + self.square / 2),
                        int(r * self.square + self.square + self.square / 2),
                    ),
                    int(self.square / 2 - 8),
                )

        for c in range(COLS):
            for r in range(ROWS):
                piece = board[r][c]
                color = RED if piece == PLAYER else YELLOW if piece == AI else None
                if color:
                    pygame.draw.circle(
                        self.screen,
                        color,
                        (
                            int(c * self.square + self.square / 2),
                            int(r * self.square + self.square + self.square / 2),
                        ),
                        int(self.square / 2 - 8),
                    )

        pygame.display.update()

    def run(self):
        game = self.game
        self.draw_board()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Player hover
                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(self.screen, BLACK, (0, 0, self.width, self.square))
                    posx = event.pos[0]
                    pygame.draw.circle(
                        self.screen, RED, (posx, int(self.square / 2)), int(self.square / 2 - 8)
                    )
                    pygame.display.update()

                # Player click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if game.turn == PLAYER:
                        posx = event.pos[0]
                        col = posx // self.square

                        result = game.make_player_move(col)
                        # draw immediately so the player's piece is visible
                        self.draw_board()
                        if result == "player_win":
                            label = self.font.render("You Win!", True, WHITE)
                            self.screen.blit(label, (40, 10))
                            pygame.display.update()
                            pygame.time.wait(3000)
                            game.reset()
                            self.draw_board()

            # AI MOVE
            if game.turn == AI and not game.game_over:
                pygame.time.wait(300)
                result = game.make_ai_move()
                # draw immediately so the AI's piece is visible before any win handling
                self.draw_board()

                if result == "ai_win":
                    label = self.font.render("AI Wins!", True, WHITE)
                    self.screen.blit(label, (40, 10))
                    pygame.display.update()
                    pygame.time.wait(3000)
                    game.reset()
                    self.draw_board()

        pygame.quit()
