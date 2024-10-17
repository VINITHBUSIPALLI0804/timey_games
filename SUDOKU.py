import random

def create_board():
    board = [[0] * 9 for _ in range(9)]
    fill_board(board)
    return board

def fill_board(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                num = random.randint(1, 9)
                if is_valid(board, num, i, j):
                    board[i][j] = num
                    if fill_board(board):
                        return True
                    board[i][j] = 0
                return False
    return True

def is_valid(board, num, row, col):
    for x in range(9):
        if board[row][x] == num or board[x][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False
    return True

def remove_numbers(board, difficulty):
    attempts = 0
    total_cells = 81
    cells_to_remove = total_cells - difficulty

    while attempts < cells_to_remove:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if board[row][col] != 0:
            board[row][col] = 0
            attempts += 1

def print_board(board):
    for row in board:
        print(" ".join(str(num) if num != 0 else '.' for num in row))

def main():
    difficulty_levels = {
        "easy": 36,
        "medium": 45,
        "hard": 54
    }

    print("Welcome to Sudoku!")
    level = input("Choose difficulty (easy, medium, hard): ").lower()

    if level not in difficulty_levels:
        print("Invalid difficulty level!")
        return

    board = create_board()
    remove_numbers(board, difficulty_levels[level])
    
    print("\nYour Sudoku Puzzle:")
    print_board(board)

if __name__ == "__main__":
    main()
