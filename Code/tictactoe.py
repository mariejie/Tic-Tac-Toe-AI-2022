import sys
import pygame
import copy
import random

WIDTH = HEIGHT = 500  # Set the window size
ROWS = COLS = 3  # Set the number of rows and columns
SQSIZE = WIDTH // COLS  # Set the size of the square
RADIUS = SQSIZE // 4  # Set the radius of the circle
OFFSET = WIDTH // 11  # Set the offset
AI_TURN = 0  # Set the AI turn

BG_COLOR = (255, 255, 255)  # White
GRID_COLOR = (172, 244, 230)  # Light Green
CIRC_COLOR = (44, 62, 80)  # Dark Blue
CROSS_COLOR = (24, 188, 156)  # Green

pygame.init()  # Initialize pygame


def go_first():  # Choose who goes first
    global AI_TURN  # Set the AI turn
    while True: # Main loop
        choice = input("Do you want to go first? (Y/n): ")  # Ask the user
        if choice.lower() == "y" or choice == "":   # If the user press Y or Enter
            AI_TURN = 2 # Set the AI turn
            break   # Break the loop
        elif choice.lower() == "n": # If the user press N
            AI_TURN = 1 # Set the AI turn
            break   # Break the loop


go_first()  # Choose who goes first

WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # Set the window size


class Board:  # Board class
    def __init__(self):  # Initialize the board
        self.block = [
            [0 for _ in range(COLS)] for _ in range(ROWS)
        ]  # Initialize the board
        self.turn = 0  # Initialize the turn

    def mark(self, row, col, player):  # Mark the board
        self.block[row][col] = player  # Mark the board
        self.turn += 1  # Increase the turn

    def is_empty_block(self, row, col):  # Check if the block is empty
        return self.block[row][col] == 0  # Check if the block is empty

    def is_full(self):  # Check if the board is full
        return self.turn == ROWS * COLS  # Check if the board is full

    def is_win(self, show_win=False):  # Check if the board is won
        for row in range(ROWS):  # Check if the row is won
            if (
                self.block[row][0] == self.block[row][1] == self.block[row][2] != 0
            ):  # Check if the row is won
                if show_win:  # Show the win line
                    WIN_COLOR = CROSS_COLOR if self.block[row][0] == 1 else CIRC_COLOR
                    pygame.draw.line(
                        WIN,
                        WIN_COLOR,
                        (WIDTH // 20, row * SQSIZE + SQSIZE // 2),
                        (WIDTH - WIDTH // 20, row * SQSIZE + SQSIZE // 2),
                        WIDTH // 40,
                    )
                return self.block[row][0]  # Return the winner

        for col in range(COLS):  # Check if the column is won
            if (
                self.block[0][col] == self.block[1][col] == self.block[2][col] != 0
            ):  # Check if the column is won
                if show_win:  # Show the win line
                    WIN_COLOR = CROSS_COLOR if self.block[0][col] == 1 else CIRC_COLOR
                    pygame.draw.line(
                        WIN,
                        WIN_COLOR,
                        (col * SQSIZE + SQSIZE // 2, WIDTH // 20),
                        (col * SQSIZE + SQSIZE // 2, HEIGHT - WIDTH // 20),
                        WIDTH // 40,
                    )
                return self.block[0][col]  # Return the winner

        if (
            self.block[0][0] == self.block[1][1] == self.block[2][2] != 0
        ):  # Check if the diagonal is won
            if show_win:  # Show the win line
                WIN_COLOR = CROSS_COLOR if self.block[0][0] == 1 else CIRC_COLOR
                pygame.draw.line(
                    WIN,
                    WIN_COLOR,
                    (WIDTH // 20, WIDTH // 20),
                    (WIDTH - WIDTH // 20, HEIGHT - WIDTH // 20),
                    WIDTH // 28,
                )
            return self.block[0][0]  # Return the winner

        if (
            self.block[0][2] == self.block[1][1] == self.block[2][0] != 0
        ):  # Check if the diagonal is won
            if show_win:  # Show the win line
                WIN_COLOR = CROSS_COLOR if self.block[0][2] == 1 else CIRC_COLOR
                pygame.draw.line(
                    WIN,
                    WIN_COLOR,
                    (WIDTH // 20, HEIGHT - WIDTH // 20),
                    (WIDTH - WIDTH // 20, WIDTH // 20),
                    WIDTH // 28,
                )
            return self.block[0][2]  # Return the winner

        return 0  # Return 0 if no one won

    def get_empty_block(self):  # Get the empty block
        block = []  # Initialize the empty block
        for row in range(ROWS):  # Get the empty block
            for col in range(COLS):  # Get the empty block
                if self.is_empty_block(row, col):  # Check if the block is empty
                    block.append((row, col))  # Append the empty block
        return block  # Return the empty block


class AI:  # AI class
    def __init__(self, player=AI_TURN):  # Initialize the AI
        self.player = player  # Initialize the AI player

    def minimax(self, board, is_maximizing):  # Minimax algorithm
        case = board.is_win()  # Check if the board is won

        if board.is_full():  # Check if the board is full
            return 0, None  # Return 0 and None
        elif case == self.player:  # Check if the AI won
            return -1, None  # Return -1 and None
        elif case == self.player % 2 + 1:  # Check if the opponent won
            return 1, None  # Return 1 and None

        if is_maximizing:
            max_score = -1000  # Initialize the max score
            best_move = None  # Initialize the best move
            for move in board.get_empty_block():  # Get the empty block
                row, col = move  # Get the empty block
                temp_board = copy.deepcopy(board)  # Copy the board
                temp_board.mark(row, col, self.player % 2 + 1)  # Mark the board
                score = self.minimax(temp_board, False)[0]  # Get the score
                if (
                    score > max_score
                ):  # Check if the score is greater than the max score
                    max_score = score  # Set the max score
                    best_move = move  # Set the best move
            return max_score, best_move  # Return the max score and the best move

        else:
            min_score = 1000  # Initialize the min score
            best_move = None  # Initialize the best move
            for move in board.get_empty_block():  # Get the empty block
                row, col = move  # Get the empty block
                temp_board = copy.deepcopy(board)  # Copy the board
                temp_board.mark(row, col, self.player)  # Mark the board
                score = self.minimax(temp_board, True)[0]  # Get the score
                if score < min_score:  # Check if the score is less than the min score
                    min_score = score  # Set the min score
                    best_move = move  # Set the best move
            return min_score, best_move  # Return the min score and the best move


class Game:  # Game class
    def __init__(self):  # Initialize the game
        self.board = Board()  # Initialize the board
        self.ai = AI()  # Initialize the AI
        self.player = 1  # Initialize the player
        self.game_over = False  # Initialize the game over
        self.draw_grid()  # Draw the grid

    def draw_grid(self):  # Draw the grid
        WIN.fill(BG_COLOR)
        pygame.draw.line(
            WIN,
            GRID_COLOR,
            (SQSIZE, WIDTH // 20),
            (SQSIZE, HEIGHT - WIDTH // 20),
            WIDTH // 40,
        )

        pygame.draw.line(
            WIN,
            GRID_COLOR,
            (SQSIZE * 2, WIDTH // 20),
            (SQSIZE * 2, HEIGHT - WIDTH // 20),
            WIDTH // 40,
        )

        pygame.draw.line(
            WIN,
            GRID_COLOR,
            (WIDTH // 20, SQSIZE),
            (WIDTH - WIDTH // 20, SQSIZE),
            WIDTH // 40,
        )

        pygame.draw.line(
            WIN,
            GRID_COLOR,
            (WIDTH // 20, SQSIZE * 2),
            (WIDTH - WIDTH // 20, SQSIZE * 2),
            WIDTH // 40,
        )

    def draw_figure(self, row, col):  # Draw the figure
        if self.player == 1:  # Check if the player is 1
            pygame.draw.line(  # Draw the cross
                WIN,
                CROSS_COLOR,
                (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET),
                (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET),
                WIDTH // 28,
            )
            pygame.draw.line(  # Draw the cross
                WIN,
                CROSS_COLOR,
                (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET),
                (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET),
                WIDTH // 28,
            )
        else:
            pygame.draw.circle(  # Draw the circle
                WIN,
                CIRC_COLOR,
                (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2),
                RADIUS,
                WIDTH // 40,
            )

    def reset(self):  # Reset the game
        self.__init__()  # Initialize the game

    def is_over(self):  # Check if the game is over
        return (
            self.board.is_full() or self.board.is_win(show_win=True) != 0
        )  # Check if the board is full or the board is won

    def make_move(self, row, col):  # Make the move
        self.board.mark(row, col, self.player)  # Mark the board
        self.draw_figure(row, col)  # Draw the figure
        self.player = (self.player % 2) + 1  # Change the player

    def winner(self):  # Get the winner
        if self.is_over() and not self.game_over:  # Check if the game is over
            self.game_over = True  # Set the game over
            if self.board.is_win(show_win=True) == AI_TURN:  # Check if the AI won
                print("AI wins")  # Print the AI wins
            elif (
                self.board.is_win(show_win=True) == AI_TURN % 2 + 1
            ):  # Check if the opponent won
                print("You wins")  # Print the You wins
            else:  # Check if the board is full
                print("Draw")  # Print the Draw
            print("Press R to reset")  # Print the Press R to reset


def main():  # Main function
    game = Game()  # Initialize the game

    while True:  # Main loop
        for event in pygame.event.get():  # Event loop
            if event.type == pygame.QUIT:  # Quit the game
                pygame.quit()  # Quit pygame
                sys.exit()  # Quit the program

            if event.type == pygame.MOUSEBUTTONDOWN and not game.is_over():
                pos = pygame.mouse.get_pos()  # Get the mouse position
                row = pos[1] // SQSIZE  # Get the row
                col = pos[0] // SQSIZE  # Get the column
                if game.player != AI_TURN and game.board.is_empty_block(
                    row, col
                ):  # Check if the block is empty
                    game.make_move(row, col)  # Make the move
                    if game.is_over():  # Check if the game is over
                        game.winner()  # Get the winner

            if event.type == pygame.KEYDOWN:  # Check if the user press the key
                if event.key == pygame.K_r:  # If the user press the R key
                    game.reset()  # Reset the game
                    game.board = Board()  # Initialize the board
                    game.ai = AI(AI_TURN)  # Initialize the AI

        if game.player == AI_TURN and not game.is_over():  # Check if the AI turn
            pygame.display.update()  # Update the display

            if game.board.turn == 0:  # Check if the board is empty
                row, col = random.choice(
                    game.board.get_empty_block()
                )  # Get the random empty block
            else:  # If the board is not empty
                row, col = game.ai.minimax(game.board, False)[1]  # Get the best move

            game.make_move(row, col)  # Make the move
            if game.is_over():  # Check if the game is over
                game.winner()  # Get the winner

        pygame.display.update()  # Update the display


main()
