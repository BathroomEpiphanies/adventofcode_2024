

def parse_input(file_handle) -> list[str]:
    return [l.strip() for l in file_handle.readlines()]


def get_rotated(matrix:list[str]) -> list[str]:
    return [''.join(matrix[i][j] for i in range(len(matrix))) for j in reversed(range(len(matrix[0])))]


def part1(problem_input:list[str]) -> int:
    total:int = 0
    matrix = problem_input
    for _ in range(4):
        for r in range(len(matrix)):
            for c in range(3, len(matrix[r])):
                if matrix[r][c-3]=='X' and matrix[r][c-2]=='M' and matrix[r][c-1]=='A' and matrix[r][c]=='S':
                    total += 1
        for r in range(3, len(matrix)):
            for c in range(3, len(matrix[r])):
                if matrix[r-3][c-3]=='X' and matrix[r-2][c-2]=='M' and matrix[r-1][c-1]=='A' and matrix[r][c]=='S':
                    total += 1
        matrix = get_rotated(matrix)
    return total


def part2(problem_input:list[str]) -> int:
    total:int = 0
    matrix = problem_input
    for _ in range(4):
        for r in range(2, len(matrix)):
            for c in range(2, len(matrix[0])):
                if matrix[r-2][c-2]=='M' and matrix[r][c-2]=='M' and matrix[r-1][c-1]=='A' and matrix[r-2][c]=='S' and matrix[r][c]=='S':
                    total += 1
        matrix = get_rotated(matrix)
    return total
