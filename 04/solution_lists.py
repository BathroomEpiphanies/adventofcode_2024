

def parse_input(file_handle) -> list[str]:
    return [l.strip() for l in file_handle.readlines()]


def count_xmas(rows:list[str]) -> int:
    sum:int = 0
    for row in rows:
        sum += row.count('XMAS')
    return sum


def get_rotated(matrix:list[str]) -> list[str]:
    return [''.join(matrix[i][j] for i in range(len(matrix))) for j in reversed(range(len(matrix[0])))]


def get_diagonals(matrix:list[str]) -> list[str]:
    diagonals  = [''.join(matrix[i][j] for i,j in zip(range(0, len(matrix)),range(c, len(matrix[0])))) for c in reversed(range(len(matrix[0])))]
    diagonals += [''.join(matrix[i][j] for i,j in zip(range(r, len(matrix)),range(0, len(matrix[0])))) for r in range(1, len(matrix))]
    return diagonals


def part1(problem_input:list[str]) -> int:
    sum:int = 0
    matrix = problem_input
    for _ in range(4):
        diagonals = get_diagonals(matrix)
        sum += count_xmas(matrix)
        sum += count_xmas(diagonals)
        matrix = get_rotated(matrix)
    return sum


def count_x_mas(rows:list[str]) -> int:
    count:int = 0
    for i,row in enumerate(rows[:-2]):
        for j,_ in enumerate(row[:-2]):
            if rows[i][j]=='M' and rows[i+2][j]=='M' and rows[i+1][j+1]=='A' and rows[i][j+2]=='S' and rows[i+2][j+2]=='S':
                count += 1
    return count


def part2(problem_input:list[str]) -> int:
    sum:int = 0
    matrix = problem_input
    for _ in range(4):
        sum += count_x_mas(matrix)
        matrix = get_rotated(matrix)
    return sum
