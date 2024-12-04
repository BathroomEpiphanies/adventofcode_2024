import numpy as np


def parse_input(file_handle:np.array):
    return np.array([list(l.strip()) for l in file_handle.readlines()], dtype='O')


def part1(problem_input) -> int:
    sum = 0
    board = problem_input
    for _ in range(4):
        rows = board[:,0:-3] + board[:,1:-2] + board[:,2:-1] + board[:,3:]
        diagonals = board[0:-3,0:-3] + board[1:-2,1:-2] + board[2:-1,2:-1] + board[3:,3:]
        sum += np.count_nonzero(rows=='XMAS')
        sum += np.count_nonzero(diagonals=='XMAS')
        board = np.rot90(board)
    return sum


def part2(problem_input) -> int:
    sum = 0
    board = problem_input
    for _ in range(4):
        crosses = (board[0:-2,0:-2] + board[2:,0:-2] + board[1:-1,1:-1] + board[0:-2,2:] + board[2:,2:])
        sum += np.count_nonzero(crosses=='MMASS')
        board = np.rot90(board)
    return sum
