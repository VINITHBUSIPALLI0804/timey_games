import pygame
import random

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 8
CELL_SIZE = WIDTH // GRID_SIZE
BACKGROUND_COLOR = (187, 173, 160)
CELL_COLOR = {
    0: (204, 192, 179),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
    4096: (237, 194, 46),  # Add color for new block
    8192: (237, 194, 46)   # Add color for new block
}

# Game class
class Game2048:
    def __init__(self):
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.spawn_new()
        self.spawn_new()
        self.score = 0

    def spawn_new(self):
        empty_cells = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if self.grid[r][c] == 0]
        if empty_cells:
            r, c = random.choice(empty_cells)
            self.grid[r][c] = random.choices([2, 4, 8, 16, 32], weights=[0.7, 0.2, 0.05, 0.025, 0.005])[0]

    def move(self, direction):
        if direction == 'UP':
            self.grid = self.transpose(self.grid)
            moved = self.slide()
            self.grid = self.transpose(self.grid)
        elif direction == 'DOWN':
            self.grid = self.transpose(self.grid)
            moved = self.slide(reverse=True)
            self.grid = self.transpose(self.grid)
        elif direction == 'LEFT':
            moved = self.slide()
        elif direction == 'RIGHT':
            moved = self.slide(reverse=True)

        if moved:
            self.spawn_new()

    def transpose(self, grid):
        return [list(row) for row in zip(*grid)]

    def slide(self, reverse=False):
        moved = False
        for r in range(GRID_SIZE):
            row = [num for num in self.grid[r] if num != 0]
            if reverse:
                row.reverse()
            new_row = []
            skip = False
            for i in range(len(row)):
                if skip:
                    skip = False
                    continue
                if i < len(row) - 1 and row[i] == row[i + 1]:
                    new_row.append(row[i] * 2)
                    self.score += row[i] * 2
                    skip = True
                else:
                    new_row.append(row[i])
            new_row += [0] * (GRID_SIZE - len(new_row))
            if reverse:
                new_row.reverse()
            if new_row != self.grid[r]:
                moved = True
            self.grid[r] = new_row
        return moved

    def is_game_over(self):
        if any(0 in row for row in self.grid):
            return False
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if (r < GRID_SIZE - 1 and self.grid[r][c] == self.grid[r + 1][c]) or \
                   (c < GRID_SIZE - 1 and self.grid[r][c] == self.grid[r][c + 1]):
                    return False
        return True

# Main function
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('2048')

    game = Game2048()
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.move('UP')
                elif event.key == pygame.K_DOWN:
                    game.move('DOWN')
                elif event.key == pygame.K_LEFT:
                    game.move('LEFT')
                elif event.key == pygame.K_RIGHT:
                    game.move('RIGHT')

        if game.is_game_over():
            print("Game Over! Press R to restart or Q to quit.")
            font = pygame.font.Font(None, 55)
            game_over_text = font.render("Game Over!", True, (255, 0, 0))
            final_score_text = font.render(f'Final Score: {game.score}', True, (255, 255, 255))
            restart_text = font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))
            
            screen.fill(BACKGROUND_COLOR)
            screen.blit(game_over_text, (WIDTH // 4, HEIGHT // 4))
            screen.blit(final_score_text, (WIDTH // 4, HEIGHT // 2))
            screen.blit(restart_text, (WIDTH // 4, HEIGHT // 1.5))
            pygame.display.flip()
            
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            game = Game2048()  # Restart the game
                            break
                        elif event.key == pygame.K_q:
                            pygame.quit()
                            return

            continue  # Break out of the event loop to redraw the new game screen

        screen.fill(BACKGROUND_COLOR)
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                value = game.grid[r][c]
                color = CELL_COLOR.get(value, (0, 0, 0))
                pygame.draw.rect(screen, color, (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                if value != 0:
                    font = pygame.font.Font(None, 55)
                    text = font.render(str(value), True, (255, 255, 255))
                    text_rect = text.get_rect(center=(c * CELL_SIZE + CELL_SIZE // 2, r * CELL_SIZE + CELL_SIZE // 2))
                    screen.blit(text, text_rect)

        # Score display
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {game.score}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(30)

if __name__ == '__main__':
    main()
