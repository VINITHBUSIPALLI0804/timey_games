import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 300, 300
LINE_WIDTH = 10
BOARD_SIZE = 3
SPACE_SIZE = WIDTH // BOARD_SIZE
FONT_SIZE = 24

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
font = pygame.font.Font(None, FONT_SIZE)

board = [[" " for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
current_player = "X"
game_over = False
winner = None

def draw_board():
    for row in range(1, BOARD_SIZE):
        pygame.draw.line(screen, BLACK, (0, row * SPACE_SIZE), (WIDTH, row * SPACE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, BLACK, (row * SPACE_SIZE, 0), (row * SPACE_SIZE, HEIGHT), LINE_WIDTH)

def draw_markers():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == "X":
                pygame.draw.line(screen, RED, (col * SPACE_SIZE + SPACE_SIZE // 4, row * SPACE_SIZE + SPACE_SIZE // 4),
                                 (col * SPACE_SIZE + SPACE_SIZE * 3 // 4, row * SPACE_SIZE + SPACE_SIZE * 3 // 4), LINE_WIDTH)
                pygame.draw.line(screen, RED, (col * SPACE_SIZE + SPACE_SIZE * 3 // 4, row * SPACE_SIZE + SPACE_SIZE // 4),
                                 (col * SPACE_SIZE + SPACE_SIZE // 4, row * SPACE_SIZE + SPACE_SIZE * 3 // 4), LINE_WIDTH)
            elif board[row][col] == "O":
                pygame.draw.circle(screen, BLUE, (col * SPACE_SIZE + SPACE_SIZE // 2, row * SPACE_SIZE + SPACE_SIZE // 2), SPACE_SIZE // 4, LINE_WIDTH)

def check_winner():
    for i in range(BOARD_SIZE):
        if board[i][0] == board[i][1] == board[i][2] != " ":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != " ":
            return board[0][i]
    
    if board[0][0] == board[1][1] == board[2][2] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != " ":
        return board[0][2]
    
    return None

def is_board_full():
    return all(cell != " " for row in board for cell in row)

def reset_game():
    global board, current_player, game_over, winner
    board = [[" " for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    current_player = "X"
    game_over = False
    winner = None

def display_winner():
    if winner:
        text = font.render(f"Player {winner} wins!", True, BLACK)
        screen.blit(text, (WIDTH // 6, HEIGHT // 2))

def main():
    global current_player, game_over, winner
    running = True

    while running:
        screen.fill(WHITE)
        draw_board()
        draw_markers()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouseX, mouseY = event.pos
                row, col = mouseY // SPACE_SIZE, mouseX // SPACE_SIZE

                if board[row][col] == " ":
                    board[row][col] = current_player
                    winner = check_winner()
                    if winner:
                        game_over = True
                    elif is_board_full():
                        game_over = True
                    current_player = "O" if current_player == "X" else "X"

            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_r:  # Press 'R' to reset the game
                    reset_game()

        if game_over:
            display_winner()

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
