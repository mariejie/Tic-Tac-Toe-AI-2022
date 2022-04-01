import sys
import pygame
import copy
import random

WIDTH = HEIGHT = 600
ROWS = COLS = 3
SQSIZE = WIDTH // COLS
RADIUS = SQSIZE // 4
OFFSET = WIDTH // 11
AI_TURN = 0

BG_COLOR = (255, 255, 255)
GRID_COLOR = (172, 244, 230)
CIRC_COLOR = (44, 62, 80)
CROSS_COLOR = (24, 188, 156)



def go_first():
    global AI_TURN
    while True:
        choice = input("Do you want to go first? (Y/n): ")
        if choice.lower() == "y" or choice == "":
            AI_TURN = 2
            break
        elif choice.lower() == "n":
            AI_TURN = 1
            break


go_first()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))


class Board:

    def __init__(self):
        self.block = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.turn = 0

    def mark(self, row, col, player):
        self.block[row][col] = player
        self.turn += 1

    def is_empty_block(self, row, col):
        return self.block[row][col] == 0

    def is_full(self):
        return self.turn == ROWS * COLS

    def is_win(self, show_win=False):
        for row in range(ROWS):
            if self.block[row][0] == self.block[row][1] == self.block[row][
                    2] != 0:
                if show_win:
                    WIN_COLOR = CROSS_COLOR if self.block[row][
                        0] == 1 else CIRC_COLOR
                    pygame.draw.line(
                        WIN,
                        WIN_COLOR,
                        (0, row * SQSIZE + SQSIZE // 2),
                        (WIDTH, row * SQSIZE + SQSIZE // 2),
                        WIDTH // 40,
                    )
                return self.block[row][0]

        for col in range(COLS):
            if self.block[0][col] == self.block[1][col] == self.block[2][
                    col] != 0:
                if show_win:
                    WIN_COLOR = CROSS_COLOR if self.block[0][
                        col] == 1 else CIRC_COLOR
                    pygame.draw.line(
                        WIN,
                        WIN_COLOR,
                        (col * SQSIZE + SQSIZE // 2, 0),
                        (col * SQSIZE + SQSIZE // 2, HEIGHT),
                        WIDTH // 40,
                    )
                return self.block[0][col]

        if self.block[0][0] == self.block[1][1] == self.block[2][2] != 0:
            if show_win:
                WIN_COLOR = CROSS_COLOR if self.block[0][0] == 1 else CIRC_COLOR
                pygame.draw.line(WIN, WIN_COLOR, (0, 0), (WIDTH, HEIGHT),
                                 WIDTH // 28)
            return self.block[0][0]

        if self.block[0][2] == self.block[1][1] == self.block[2][0] != 0:
            if show_win:
                WIN_COLOR = CROSS_COLOR if self.block[0][2] == 1 else CIRC_COLOR
                pygame.draw.line(WIN, WIN_COLOR, (0, HEIGHT), (WIDTH, 0),
                                 WIDTH // 28)
            return self.block[0][2]

        return 0

    def get_empty_block(self):
        block = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.is_empty_block(row, col):
                    block.append((row, col))
        return block


class AI:

    def __init__(self, player=AI_TURN):
        self.player = player

    def minimax(self, board, is_maximizing):
        case = board.is_win()

        if board.is_full():
            return 0, None
        elif case == self.player:
            return -1, None
        elif case == 3 - self.player:
            return 1, None

        if is_maximizing:
            max_score = -1000
            best_move = None
            for move in board.get_empty_block():
                row, col = move
                temp_board = copy.deepcopy(board)
                temp_board.mark(row, col, 3 - self.player)
                score = self.minimax(temp_board, False)[0]
                if score > max_score:
                    max_score = score
                    best_move = move
            return max_score, best_move

        else:
            min_score = 1000
            best_move = None
            for move in board.get_empty_block():
                row, col = move
                temp_board = copy.deepcopy(board)
                temp_board.mark(row, col, self.player)
                score = self.minimax(temp_board, True)[0]
                if score < min_score:
                    min_score = score
                    best_move = move
            return min_score, best_move


class Game:

    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1
        self.game_over = False
        self.draw_grid()

    def draw_grid(self):
        WIN.fill(BG_COLOR)
        for x in range(SQSIZE, WIDTH, SQSIZE):
            pygame.draw.line(WIN, GRID_COLOR, (x, WIDTH // 28),
                             (x, HEIGHT - WIDTH // 28), WIDTH // 40)
        for y in range(SQSIZE, HEIGHT, SQSIZE):
            pygame.draw.line(WIN, GRID_COLOR, (WIDTH // 28, y),
                             (WIDTH - WIDTH // 28, y), WIDTH // 40)

    def draw_figure(self, row, col):
        if self.player == 1:
            pygame.draw.line(
                WIN,
                CROSS_COLOR,
                (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET),
                (col * SQSIZE + SQSIZE - OFFSET,
                 row * SQSIZE + SQSIZE - OFFSET),
                WIDTH // 28,
            )
            pygame.draw.line(
                WIN,
                CROSS_COLOR,
                (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET),
                (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET),
                WIDTH // 28,
            )
        else:
            pygame.draw.circle(
                WIN,
                CIRC_COLOR,
                (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2),
                RADIUS,
                WIDTH // 40,
            )

    def reset(self):
        self.__init__()

    def is_over(self):
        return self.board.is_full() or self.board.is_win(show_win=True) != 0

    def make_move(self, row, col):
        self.board.mark(row, col, self.player)
        self.draw_figure(row, col)
        self.player = (self.player % 2) + 1

    def winner(self):
        if self.is_over() and not self.game_over:
            self.game_over = True
            if self.board.is_win() == AI_TURN:
                print("AI wins")
            elif self.board.is_win() == 3 - AI_TURN:
                print("You wins")
            else:
                print("Draw")
            print("Press R to reset")


def main():
    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE
                if game.board.is_empty_block(row, col) and not game.is_over():
                    game.make_move(row, col)
                    game.winner()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.reset()
                    AI_TURN = 0
                    while True:
                        go_first = input("Do you want to go first? (Y/n): ")
                        if go_first.lower() == "y" or go_first == "":
                            AI_TURN = 2
                            break
                        elif go_first == "n":
                            AI_TURN = 1
                            break
                    game.board = Board()
                    game.ai = AI(AI_TURN)

        if game.player == game.ai.player and not game.game_over:
            pygame.display.update()

            if game.board.turn == 0:
                row, col = random.choice(game.board.get_empty_block())
            else:
                row, col = game.ai.minimax(game.board, False)[1]

            game.make_move(row, col)
            game.winner()

        pygame.display.update()


main()
