import pygame
import sys
import time
import copy

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

pygame.init()

SCREEN_WIDTH = 540
SCREEN_HEIGHT = 540
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sudoku Solver")

GRID_SIZE = SCREEN_WIDTH // 9
FONT_SIZE = 40
font = pygame.font.Font(None, FONT_SIZE)

# Define backtrack_count as a global variable
backtrack_count = 0

def is_valid(board, row, col, num):
    for x in range(9):
        if board[row][x] == num:
            return False

    for x in range(9):
        if board[x][col] == num:
            return False

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False

    return True

def find_empty_location(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return -1, -1

def solve_sudoku(board):
    global backtrack_count  # Declare backtrack_count as global
    row, col = find_empty_location(board)

    # If there are no empty locations, puzzle is solved
    if row == -1 and col == -1:
        return True

    for num in range(1, 10):
        backtrack_count += 1
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0  # Backtrack if the solution is not found

    return False

def draw_board(board):
    screen.fill(WHITE)
    for i in range(9):
        for j in range(9):
            cell_color = WHITE if board[i][j] == 0 else GRAY
            pygame.draw.rect(screen, cell_color, (j * GRID_SIZE, i * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            if board[i][j] != 0:
                text = font.render(str(board[i][j]), True, BLACK)
                screen.blit(text, (j * GRID_SIZE + GRID_SIZE // 3, i * GRID_SIZE + GRID_SIZE // 4))

    for i in range(10):
        if i % 3 == 0:
            pygame.draw.line(screen, BLACK, (0, i * GRID_SIZE), (SCREEN_WIDTH, i * GRID_SIZE), 2)
            pygame.draw.line(screen, BLACK, (i * GRID_SIZE, 0), (i * GRID_SIZE, SCREEN_HEIGHT), 2)
        else:
            pygame.draw.line(screen, BLACK, (0, i * GRID_SIZE), (SCREEN_WIDTH, i * GRID_SIZE), 1)
            pygame.draw.line(screen, BLACK, (i * GRID_SIZE, 0), (i * GRID_SIZE, SCREEN_HEIGHT), 1)

    pygame.display.flip()

def main():
    # sudoku_board = [
    #     [5, 3, 0, 0, 7, 0, 0, 0, 0],
    #     [6, 0, 0, 1, 9, 5, 0, 0, 0],
    #     [0, 9, 8, 0, 0, 0, 0, 6, 0],
    #     [8, 0, 0, 0, 6, 0, 0, 0, 3],
    #     [4, 0, 0, 8, 0, 3, 0, 0, 1],
    #     [7, 0, 0, 0, 2, 0, 0, 0, 6],
    #     [0, 6, 0, 0, 0, 0, 2, 8, 0],
    #     [0, 0, 0, 4, 1, 9, 0, 0, 5],
    #     [0, 0, 0, 0, 8, 0, 0, 7, 9]
    # ]
    sudoku_board = [
    [0, 0, 0, 2, 6, 0, 7, 0, 1],
    [6, 8, 0, 0, 7, 0, 0, 9, 0],
    [1, 9, 0, 0, 0, 4, 5, 0, 0],
    [8, 2, 0, 1, 0, 0, 0, 4, 0],
    [0, 0, 4, 6, 0, 2, 9, 0, 0],
    [0, 5, 0, 0, 0, 3, 0, 2, 8],
    [0, 0, 9, 3, 0, 0, 0, 7, 4],
    [0, 4, 0, 0, 5, 0, 0, 3, 6],
    [7, 0, 3, 0, 1, 8, 0, 0, 0]
]

    draw_board(sudoku_board)

    unsolved_shown = True
    solved_board = None

    while True:
        global backtrack_count
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if unsolved_shown:
                        start_time = time.time()
                        solved_board = copy.deepcopy(sudoku_board)
                        solve_sudoku(solved_board)
                        end_time = time.time()
                        print("Time taken to solve Sudoku:", end_time - start_time, "seconds")
                        print("Number of backtracking steps:", backtrack_count)
                        draw_board(solved_board)
                        unsolved_shown = False
                    else:
                        draw_board(sudoku_board)
                        unsolved_shown = True
                        backtrack_count = 0


if __name__ == "__main__":
    main()
