import re

from dataclasses import dataclass
from more_itertools import grouper


@dataclass
class Coord:
    x:int
    y:int

@dataclass
class Machine:
    A:Coord
    B:Coord
    P:Coord
    def cost_to_win(self, offset:int=0) -> int:
        """
        Solve the system:
        a*A.dx + a*B.dx = prize.x
        b*A.dy + b*B.dy = prize.y
        an/ad: numerator and denominator of contant a
        """
        an,ad = a = ((offset+self.P.x)*self.B.y-self.B.x*(offset+self.P.y)), (self.A.x*self.B.y-self.B.x*self.A.y)
        bn,bd = b = ((offset+self.P.x)*self.A.y-self.A.x*(offset+self.P.y)), (self.B.x*self.A.y-self.A.x*self.B.y)
        if an%ad==0 and bn%bd==0:
            return 3*(an//ad) + (bn//bd)
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
