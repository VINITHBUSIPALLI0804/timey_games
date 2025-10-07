import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dots and Boxes")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
BLUE = (65, 105, 225)
GRAY = (200, 200, 200)

# Grid settings
ROWS, COLS = 5, 5  # Number of dots per row and column
DOT_RADIUS = 6
DOT_SPACING = 100  # pixels between dots
START_X, START_Y = 50, 50

# Player colors
PLAYER_COLORS = [RED, BLUE]

# Initialize line and box data structures
horizontal_lines = [[False] * (COLS - 1) for _ in range(ROWS)]
vertical_lines = [[False] * COLS for _ in range(ROWS - 1)]
boxes = [[-1] * (COLS - 1) for _ in range(ROWS - 1)]  # -1 = unclaimed, else player index

font = pygame.font.SysFont(None, 36)

def draw_board():
    screen.fill(WHITE)
    # Draw dots
    for row in range(ROWS):
        for col in range(COLS):
            x = START_X + col * DOT_SPACING
            y = START_Y + row * DOT_SPACING
            pygame.draw.circle(screen, BLACK, (x, y), DOT_RADIUS)

    # Draw horizontal lines
    for row in range(ROWS):
        for col in range(COLS - 1):
            x1 = START_X + col * DOT_SPACING
            y1 = START_Y + row * DOT_SPACING
            if horizontal_lines[row][col]:
                pygame.draw.line(screen, PLAYER_COLORS[horizontal_lines[row][col]-1],
                                 (x1, y1), (x1 + DOT_SPACING, y1), 6)
            else:
                pygame.draw.line(screen, GRAY,
                                 (x1, y1), (x1 + DOT_SPACING, y1), 2)

    # Draw vertical lines
    for row in range(ROWS - 1):
        for col in range(COLS):
            x1 = START_X + col * DOT_SPACING
            y1 = START_Y + row * DOT_SPACING
            if vertical_lines[row][col]:
                pygame.draw.line(screen, PLAYER_COLORS[vertical_lines[row][col]-1],
                                 (x1, y1), (x1, y1 + DOT_SPACING), 6)
            else:
                pygame.draw.line(screen, GRAY,
                                 (x1, y1), (x1, y1 + DOT_SPACING), 2)

    # Draw boxes
    for row in range(ROWS - 1):
        for col in range(COLS - 1):
            if boxes[row][col] != -1:
                x = START_X + col * DOT_SPACING + DOT_SPACING // 2
                y = START_Y + row * DOT_SPACING + DOT_SPACING // 2
                pygame.draw.rect(screen, PLAYER_COLORS[boxes[row][col]], 
                                 (x - DOT_SPACING//2 + 10, y - DOT_SPACING//2 + 10, DOT_SPACING - 20, DOT_SPACING - 20))
                
def check_complete_box(row, col, player):
    completed = False
    # Check all boxes adjacent to the line and claim if complete.
    # Horizontal line check
    if row > 0 and all([horizontal_lines[row][col], horizontal_lines[row-1][col],
                       vertical_lines[row-1][col], vertical_lines[row-1][col+1]]):
        if boxes[row-1][col] == -1:
            boxes[row-1][col] = player
            completed = True
    if row < ROWS -1 and all([horizontal_lines[row][col], horizontal_lines[row+1][col],
                            vertical_lines[row][col], vertical_lines[row][col+1]]):
        if boxes[row][col] == -1:
            boxes[row][col] = player
            completed = True
    # Vertical line check
    if col > 0 and all([vertical_lines[row][col], vertical_lines[row][col-1],
                      horizontal_lines[row][col-1], horizontal_lines[row+1][col-1]]):
        if boxes[row][col-1] == -1:
            boxes[row][col-1] = player
            completed = True
    if col < COLS - 1 and all([vertical_lines[row][col], vertical_lines[row][col+1],
                             horizontal_lines[row][col], horizontal_lines[row+1][col]]):
        if boxes[row][col] == -1:
            boxes[row][col] = player
            completed = True
    return completed

def update_score():
    scores = [0, 0]
    for row in range(ROWS - 1):
        for col in range(COLS - 1):
            if boxes[row][col] != -1:
                scores[boxes[row][col]] += 1
    return scores

def get_line_clicked(pos):
    x, y = pos
    # Check near horizontal lines
    for row in range(ROWS):
        for col in range(COLS - 1):
            x1 = START_X + col * DOT_SPACING
            y1 = START_Y + row * DOT_SPACING
            if (x1 - 10 <= x <= x1 + DOT_SPACING + 10) and (y1 - 10 <= y <= y1 + 10):
                if not horizontal_lines[row][col]:
                    return ('h', row, col)
    # Check near vertical lines
    for row in range(ROWS - 1):
        for col in range(COLS):
            x1 = START_X + col * DOT_SPACING
            y1 = START_Y + row * DOT_SPACING
            if (x1 - 10 <= x <= x1 + 10) and (y1 - 10 <= y <= y1 + DOT_SPACING + 10):
                if not vertical_lines[row][col]:
                    return ('v', row, col)
    return None

def main():
    running = True
    current_player = 0
    scores = [0, 0]

    while running:
        draw_board()
        # Display scores and turn info
        score_text = font.render(f"Red: {scores[0]}    Blue: {scores[1]}", True, BLACK)
        turn_text = font.render(f"Turn: {'Red' if current_player == 0 else 'Blue'}", True, BLACK)
        screen.blit(score_text, (50, HEIGHT - 80))
        screen.blit(turn_text, (WIDTH - 200, HEIGHT - 80))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = get_line_clicked(event.pos)
                if click:
                    line_type, row, col = click
                    if line_type == 'h':
                        horizontal_lines[row][col] = current_player + 1
                    else:
                        vertical_lines[row][col] = current_player + 1

                    # Check if box(es) completed - if yes, same player gets extra turn
                    if check_complete_box(row, col, current_player):
                        scores = update_score()
                    else:
                        current_player = (current_player + 1) % 2

                    scores = update_score()

        # Check if all boxes filled (game over)
        if sum(scores) == (ROWS - 1) * (COLS - 1):
            running = False

    # Game over display
    screen.fill(WHITE)
    draw_board()
    scores = update_score()
    winner_text = "Draw"
    if scores[0] > scores[1]:
        winner_text = "Red Wins!"
    elif scores[1] > scores[0]:
        winner_text = "Blue Wins!"
    win_display = font.render(winner_text, True, BLACK)
    score_display = font.render(f"Final Scores - Red: {scores[0]}  Blue: {scores[1]}", True, BLACK)
    screen.blit(win_display, (WIDTH//2 - win_display.get_width()//2, HEIGHT//2 - 50))
    screen.blit(score_display, (WIDTH//2 - score_display.get_width()//2, HEIGHT//2 + 10))
    pygame.display.flip()

    pygame.time.wait(5000)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
