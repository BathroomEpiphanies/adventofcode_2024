from functools import cache
from more_itertools import ilen
from typing import Callable


def parse_input(file_handle) -> tuple[list[str],list[str]]:
    lines = (l.strip() for l in file_handle.readlines())
    towels = next(lines).split(', ')
    next(lines)
    designs = [l for l  in lines]
    return towels,designs


def create_design_finder(towels:list[str]) -> Callable[[str], int]:
    @cache
    def __function(design:str) -> int:
        if design == '':
            return 1
        else:
            return sum(
                __function(design.removeprefix(t))
                for t in towels if design.startswith(t)
            )
    return __function


def part1(problem_input:tuple[list[str],list[str]]) -> int:
    towels,designs = problem_input
    towel_pattern_finder = create_design_finder(towels)
    return ilen(p for p in designs if towel_pattern_finder(p)>0)


def part2(problem_input:tuple[list[str],list[str]]) -> int:
    towels,designs = problem_input
    towel_pattern_finder = create_design_finder(towels)
    return sum(towel_pattern_finder(p) for p in designs)
