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
pygame.display.set_caption("Improved Sudoku Solver")

GRID_SIZE = SCREEN_WIDTH // 9
FONT_SIZE = 40
font = pygame.font.Font(None, FONT_SIZE)

# Counter to track the number of backtracking steps
backtrack_count = 0


def is_valid(board, row, col, num):
    """
    Check if placing a number in a cell is valid.
    """
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
    """
    Find the first empty cell in the board.
    """
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return -1, -1


def solve_sudoku(board):
    """
    Solve the Sudoku puzzle using backtracking with forward checking and MAC.
    """
    global backtrack_count
    empty_cells = order_empty_cells(board)
    backtrack_count = 0  # Reset the backtrack counter
    return backtrack(board, empty_cells)


def order_empty_cells(board):
    """
      Order empty cells based on the number of possible values and number  of constraining variables.
      """
    empty_cells = []
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                empty_cells.append((i, j))
    empty_cells.sort(
        key=lambda cell: (len(possible_values(board, *cell)), cell))  # Both Variable and value ordering is done
    return empty_cells


def possible_values(board, row, col):
    """
      Get the possible values for a cell.
    """
    row_values = set(board[row])
    col_values = set(board[i][col] for i in range(9))

    box_values = set()
    box_row_start = (row // 3) * 3
    box_col_start = (col // 3) * 3
    for i in range(box_row_start, box_row_start + 3):
        for j in range(box_col_start, box_col_start + 3):
            box_values.add(board[i][j])

    return set(range(1, 10)) - row_values - col_values - box_values


def least_constraining_value(board, row, col):
    """
       Get the least constraining value for a cell.
    """
    values = possible_values(board, row, col)
    constraints = []
    for value in values:
        constraint_count = count_constraints(board, row, col, value)
        constraints.append((value, constraint_count))
    return sorted(constraints, key=lambda x: x[1])


def count_constraints(board, row, col, value):
    """
    Count the number of constraints for a value in a cell.
    """
    constraints = 0
    for i in range(9):
        if board[row][i] == 0 and value in possible_values(board, row, i):
            constraints += 1
        if board[i][col] == 0 and value in possible_values(board, i, col):
            constraints += 1
    box_row, box_col = row // 3 * 3, col // 3 * 3
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if board[i][j] == 0 and value in possible_values(board, i, j):
                constraints += 1
    return constraints

def forward_check(board, row, col, value):
    # Perform forward checking
    for i in range(9):
        if i != col and board[row][i] == 0:  # Exclude the current cell
            if not mac(board, row, i, value):
                return False
        if i != row and board[i][col] == 0:  # Exclude the current cell
            if not mac(board, i, col, value):
                return False
    box_row_start, box_col_start = (row // 3) * 3, (col // 3) * 3
    for i in range(box_row_start, box_row_start + 3):
        for j in range(box_col_start, box_col_start + 3):
            if i != row and j != col and board[i][j] == 0:  # Exclude the current cell
                if not mac(board, i, j, value):
                    return False
    return True


def mac(board, row, col, value):
    """
     Perform Maintaining Arc Consistency (MAC) algorithm
      Returns:
        domain_changed (bool): True if any domain was changed during the MAC algorithm, False otherwise.
    """
    domain_changed = False
    for val in possible_values(board, row, col):
        if val != value:
            domain_changed = True
            board[row][col] = val
            if not is_valid(board, row, col, val):
                board[row][col] = 0
            else:
                board[row][col] = value
                return True
    return domain_changed


def backtrack(board, empty_cells):
    """
     Backtracking algorithm to solve the Sudoku puzzle.
     """
    global backtrack_count
    if not empty_cells:
        return True

    row, col = empty_cells[0]
    for value, _ in least_constraining_value(board, row, col):
        backtrack_count += 1  # Increment backtrack counter
        if is_valid(board, row, col, value):
            board[row][col] = value
            forward_check(board, row, col, value)
            if backtrack(board, empty_cells[1:]):
                return True
            board[row][col] = 0
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
    sudoku_board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    draw_board(sudoku_board)
    unsolved_shown = True

    while True:
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


if __name__ == "__main__":
    main()
