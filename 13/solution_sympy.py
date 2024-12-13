import re

from dataclasses import dataclass
from more_itertools import grouper

from sympy import solve
from sympy.abc import a,b
from sympy.core.numbers import Integer as sympyInt


@dataclass
class Coord:
    x:int
    y:int

@dataclass
class Machine:
    A:Coord
    B:Coord
    prize:Coord
    def cost_to_win(self, offset:int=0) -> int:
        solution = solve(
            [a*self.A.x + b*self.B.x - (offset+self.prize.x),
             a*self.A.y + b*self.B.y - (offset+self.prize.y)],
            [a,b]
        )
        na,nb = solution[a],solution[b]
        if isinstance(na, sympyInt) and isinstance(nb, sympyInt):
            return 3*na + nb
        else:
            return 0


def parse_input(file_handle) -> list[Machine]:
    def __parse_line(line:str) -> Coord:
        gs = re.match(r'(?:Button [A|B]|Prize): X[=+]([0-9]+), Y[=+]([0-9]+)', line).groups()
        return Coord(int(gs[0]), int(gs[1]))
    machines:list[Machine] = []
    for *lines,_ in grouper((l.strip() for l in file_handle.readlines()), 4):
        machines.append(Machine(*(__parse_line(l) for l in lines)))
    return machines


def part1(problem_input:list[Machine]) -> int:
    return sum(machine.cost_to_win() for machine in problem_input)


def part2(problem_input:list[Machine]) -> int:
    return sum(machine.cost_to_win(offset=10_000_000_000_000) for machine in problem_input)
