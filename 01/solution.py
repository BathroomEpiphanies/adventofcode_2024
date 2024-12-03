import re


def parse_input(file_handle) -> tuple[list[int],list[int]]:
    l = [re.split(r' +', l) for l in file_handle.readlines()]
    return [int(a) for a,_ in l],[int(b) for _,b in l]


def part1(problem_input:tuple[list[int],list[int]]) -> int:
    sum:int = 0
    first,second = problem_input
    for a,b in zip(sorted(first),sorted(second)):
        sum += abs(b-a)
    return sum


def part2(problem_input:tuple[list[int],list[int]]) -> int:
    sum:int = 0
    for a in problem_input[0]:
        sum += a*problem_input[1].count(a)
    return sum
