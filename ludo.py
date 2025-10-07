import pygame
import random
import sys
import time

pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ludo Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
GREEN = (50, 205, 50)
BLUE = (65, 105, 225)
YELLOW = (255, 215, 0)
GREY = (200, 200, 200)

# Board settings
CELL_SIZE = 40
BOARD_ORIGIN = (50, 50)

# Positions of squares in Ludo path (simplified linear path for demo)
PATH_POSITIONS = []
for i in range(15):
    PATH_POSITIONS.append((BOARD_ORIGIN[0] + i * CELL_SIZE, BOARD_ORIGIN[1]))
for i in range(1, 15):
    PATH_POSITIONS.append((BOARD_ORIGIN[0] + 14 * CELL_SIZE, BOARD_ORIGIN[1] + i * CELL_SIZE))
for i in range(1, 15):
    PATH_POSITIONS.append((BOARD_ORIGIN[0] + (14 - i) * CELL_SIZE, BOARD_ORIGIN[1] + 14 * CELL_SIZE))
for i in range(1, 14):
    PATH_POSITIONS.append((BOARD_ORIGIN[0], BOARD_ORIGIN[1] + (14 - i) * CELL_SIZE))

# Token start positions (home)
PLAYERS_START = {
    'red': [(BOARD_ORIGIN[0] + i * CELL_SIZE, BOARD_ORIGIN[1] + CELL_SIZE * 15) for i in range(4)],
    'green': [(BOARD_ORIGIN[0] + CELL_SIZE * 15, BOARD_ORIGIN[1] + i * CELL_SIZE) for i in range(4)],
}

# Token colors
TOKEN_COLORS = {
    'red': RED,
    'green': GREEN
}

# Dice font
font = pygame.font.SysFont(None, 36)

class Token:
    def __init__(self, color, start_pos, path):
        self.color = color
        self.path = path
        self.position_index = -1  # -1 means at home
        self.x, self.y = start_pos
        self.radius = 15
        self.home_pos = start_pos
    
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x + CELL_SIZE//2, self.y + CELL_SIZE//2), self.radius)

    def move_steps(self, steps):
        if self.position_index + steps < len(self.path):
            self.position_index += steps
            self.x, self.y = self.path[self.position_index]
        else:
            # Can't move beyond last position
            pass

    def is_finished(self):
        return self.position_index == len(self.path) - 1

    def at_home(self):
        return self.position_index == -1

    def move_from_home(self):
        # Move token from home to start path pos (0 index)
        if self.position_index == -1:
            self.position_index = 0
            self.x, self.y = self.path[0]

def draw_board():
    screen.fill(WHITE)
    # Draw path squares
    for pos in PATH_POSITIONS:
        pygame.draw.rect(screen, GREY, (pos[0], pos[1], CELL_SIZE, CELL_SIZE), 2)
    # Draw home areas for red and green players
    for pos in PLAYERS_START['red']:
        pygame.draw.rect(screen, RED, (pos[0], pos[1], CELL_SIZE, CELL_SIZE))
    for pos in PLAYERS_START['green']:
        pygame.draw.rect(screen, GREEN, (pos[0], pos[1], CELL_SIZE, CELL_SIZE))

def roll_dice():
    return random.randint(1, 6)

def display_dice(value):
    dice_text = font.render(f'Dice: {value}', True, BLACK)
    screen.blit(dice_text, (400, 50))

def main():
    clock = pygame.time.Clock()

    # Create tokens for two players (1 token each for simplicity)
    red_token = Token(RED, PLAYERS_START['red'][0], PATH_POSITIONS)
    green_token = Token(GREEN, PLAYERS_START['green'][0], PATH_POSITIONS)

    players = [('Red', red_token), ('Green', green_token)]
    current_player = 0

    dice_value = 0
    move_allowed = False

    running = True
    while running:
        draw_board()
        red_token.draw(screen)
        green_token.draw(screen)

        display_dice(dice_value)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not move_allowed:
                    # Roll dice
                    dice_value = roll_dice()
                    print(f"{players[current_player][0]} rolled {dice_value}")
                    move_allowed = True
                
                elif event.key == pygame.K_RETURN and move_allowed:
                    # Move token
                    token = players[current_player][1]
                    # If token at home, must roll 6 to enter path
                    if token.at_home():
                        if dice_value == 6:
                            token.move_from_home()
                        else:
                            print(f"{players[current_player][0]} must roll 6 to start")
                    else:
                        token.move_steps(dice_value)
                    
                    if token.is_finished():
                        print(f"{players[current_player][0]} wins!")
                        running = False
                    
                    # Switch turn unless rolled 6
                    if dice_value != 6:
                        current_player = (current_player + 1) % len(players)
                    move_allowed = False

        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
