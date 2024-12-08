from typing import Callable, Iterable

from collections import defaultdict
from itertools import count, permutations


def parse_input(file_handle) -> tuple[dict[str,list[complex]],tuple[int,int]]:
    antennas = defaultdict(list)
    for r,row in enumerate(l.strip() for l in file_handle.readlines()):
        for c,p in enumerate(row):
            if p!='.':
                antennas[p].append(c+r*1j)
        width = c+1
    height = r+1
    return dict(antennas),(width,height)


def antinodes_in_area(
    antennas:dict[str,list[complex]],
    width:int,
    height:int,
    wavelengths:Callable[[],Iterable[int]],
) -> set[complex]:
    antinodes:set[complex] = set()
    for _,locations in antennas.items():
        for l1,l2 in permutations(locations, r=2):
            for n in wavelengths():
                antinode = l1+n*(l2-l1)
                if 0<=antinode.real<width and 0<=antinode.imag<height:
                    antinodes.add(antinode)
                else:
                    break
    return antinodes


def part1(problem_input:tuple[dict[str,list[complex]],tuple[int,int]]) -> int:
    antennas,(width,height) = problem_input
    return len(antinodes_in_area(antennas, width, height, lambda: [2]))


def part2(problem_input:tuple[dict[str,list[complex]],tuple[int,int]]) -> int:
    antennas,(width,height) = problem_input
    return len(antinodes_in_area(antennas, width, height, count))
