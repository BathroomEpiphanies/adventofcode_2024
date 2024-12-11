from functools import cache


def parse_input(file_handle) -> list[int]:
    return [int(n) for n in file_handle.readline().strip().split(' ')]


@cache
def stone_counter(engraving:int, iterations:int) -> int:
    if iterations == 0:
        return 1
    elif engraving == 0:
        return stone_counter(1, iterations-1)
    elif len(stone_:=str(engraving))%2 == 0:
        a = int(stone_[:len(stone_)//2])
        b = int(stone_[len(stone_)//2:])
        return stone_counter(a, iterations-1) + \
               stone_counter(b, iterations-1)
    else:
        return stone_counter(engraving*2024, iterations-1)


def part1(problem_input:list[int]) -> int:
    return sum(stone_counter(s, 25) for s in problem_input)


def part2(problem_input:list[int]) -> int:
    return sum(stone_counter(s, 75) for s in problem_input)
