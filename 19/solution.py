from functools import cache
from more_itertools import ilen
from typing import Callable


def parse_input(file_handle) -> tuple[list[str],list[str]]:
    lines = (l.strip() for l in file_handle.readlines())
    towels = next(lines).split(', ')
    next(lines)
    patterns = [l for l  in lines]
    return towels,patterns


def create_towel_finder(towels:list[str]) -> Callable[[str,str], int]:
    @cache
    def __fun(pattern:str, towel:str='') -> int:
        if pattern == towel:
            return 1
        elif pattern.startswith(towel):
            return sum(__fun(pattern.removeprefix(towel), t) for t in towels)
        else:
            return 0
    return __fun


def part1(problem_input:tuple[list[str],list[str]]) -> int:
    towels,patterns = problem_input
    towel_pattern_finder = create_towel_finder(towels)
    return ilen(p for p in patterns if towel_pattern_finder(p, '')>0)


def part2(problem_input:tuple[list[str],list[str]]) -> int:
    towels,patterns = problem_input
    towel_pattern_finder = create_towel_finder(towels)
    return sum(towel_pattern_finder(p, '') for p in patterns)
