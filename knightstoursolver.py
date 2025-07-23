from sys import argv
from datetime import datetime

# functions to filter symmetries
def rotate_90(board):
    return [list(row) for row in zip(*board[::-1])]

def flip_horizontal(board):
    return [row[::-1] for row in board]

def flip_vertical(board):
    return board[::-1]

def transpose(board):
    return [list(row) for row in zip(*board)]

def reflect_main_diagonal(board):
    return transpose(board)

def reflect_anti_diagonal(board):
    return rotate_90(transpose(board))

def generate_symmetries(board):
    symmetries = set()
    transforms = [
        lambda b: b,
        rotate_90,
        flip_horizontal,
        flip_vertical,
        reflect_main_diagonal,
        reflect_anti_diagonal
    ]
    for transform in transforms:
        transformed = transform(board)
        symmetries.add(tuple(tuple(row) for row in transformed))
    return symmetries

def filter_unique_solutions(solutions):
    unique = []
    seen = set()
    for solution in solutions:
        board_tuple_forms = generate_symmetries(solution[2])
        if not seen.intersection(board_tuple_forms):
            seen.update(board_tuple_forms)
            unique.append(solution)
    return unique

# Main functions
def copy_branch(branch): # function to replace copy.deepcopy since it's slow
    x, y, board = branch
    new_board = [row[:] for row in board]
    return [x, y, new_board]

def copy_solutions(solutions): # also a function to replace copy.deepcopy, but for nested lists
    new_solutions = []
    for x, y, board in solutions:
        new_board = [row[:] for row in board]  # Fast 2D board copy
        new_solutions.append([x, y, new_board])
    return new_solutions

def initialize_board(width, height):
    return [[-1 for _ in range(width)] for _ in range(height)]

def is_valid_move(x, y, board, width, height):
    return 0 <= x < width and 0 <= y < height and board[y][x] == -1

def solve(board, start_x, start_y, width, height): # Non-recursive function to solve the knights tour, to save on memory
    solutions = [[start_x, start_y, board]]

    knight_moves = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
    
    move_count = 1
    
    while True:
        move_count += 1
        solutions_original = copy_solutions(solutions)
        for branch in solutions_original:
            for dx, dy in knight_moves:
                x = branch[0]
                y = branch[1]
                new_x, new_y = x + dx, y + dy
                if is_valid_move(new_x, new_y, branch[2], width, height):
                    templist = copy_branch(branch)
                    templist[2][new_y][new_x] = move_count
                    templist[0] = new_x
                    templist[1] = new_y
                    solutions.append(templist)
            solutions.remove(branch)
        if len(solutions) == 0:
            break
        if move_count >= width*height:
            break
        solutions = filter_unique_solutions(solutions)
    
    return solutions

def printable_board(board):
    output = ""
    for row in board:
        output += (' '.join(str(cell).rjust(3, ' ') for cell in row)) + "\n"
    return output

def main():
    if len(argv) != 3:
        print("Usage: %s width height"%argv[0])
        exit(0)
    width = int(argv[1])
    height = int(argv[2])
    init_board = initialize_board(width, height)
    
    start_x, start_y = 0, 0  # Starting position of the knight
    init_board[start_x][start_y] = 1  # Initialize the starting position with the first move
    
    solutions = solve(init_board, start_x, start_y, width, height)
    
    if len(solutions) > 0:
        # Hacky one-liner to pluralise "Solution" if there is more than one
        print("1 Solution found" if len(solutions)==1 else "%d Solutions found"%len(solutions))
        
        file_output = ""
        for solution in solutions[:200]:
            file_output += printable_board(solution[2])
            file_output += "\n"
        
        # Output data into a file with the current time as the name
        now = datetime.now()
        filename = "outputs/output-%s.txt"%str(now.strftime("%Y-%m-%d-%H-%M-%S"))
        with open(filename, "w") as file:
            file.write(file_output)

        if len(solutions) > 200:
            print("Ommiting %d solutions, more than 200 solutions detected."%(len(solutions)-200))
    else:
        print("No solution exists")

if __name__ == "__main__":
    main()