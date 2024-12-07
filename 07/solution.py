from dataclasses import dataclass
from itertools import product
from operator import add, mul


@dataclass
class Equation:
    result:int
    operands:tuple[int,...]


def parse_input(file_handle) -> list[Equation]:
    equations = []
    for line in (l.strip() for l in file_handle.readlines()):
        result,operands = line.split(': ')
        equations.append(Equation(int(result),tuple(int(o) for o in operands.split(' '))))
    return equations


def equation_is_satisfiable(equation:Equation, operators:list[callable]) -> bool:
    for __operators in product(operators, repeat=len(equation.operands[1:])):
        result = equation.operands[0]
        for operand,__operator in zip(equation.operands[1:], __operators):
            result = __operator(result, operand)
        if result==equation.result:
            return True
    return False


def part1(problem_input:list[Equation]) -> int:
    return sum(e.result for e in problem_input if equation_is_satisfiable(e, [add,mul]))


def concat(a:int, b:int) -> int:
    return int(f'{a}{b}')


def part2(problem_input:list[str]) -> int:
    return sum(e.result for e in problem_input if equation_is_satisfiable(e, [add,mul,concat]))
