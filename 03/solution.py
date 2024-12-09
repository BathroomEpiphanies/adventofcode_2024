import re


def parse_input(file_handle) -> str:
    return ''.join(l.strip() for l in file_handle.readlines())


def part1(problem_input:str) -> int:
    total:int = 0
    multiplications = re.findall(r'mul\(([0-9]+),([0-9]+)\)', problem_input)
    for multiplication in multiplications:
        total += int(multiplication[0])*int(multiplication[1])
    return total


def part2(problem_input:str) -> int:
    total:int = 0
    do_strings = [d.split('don\'t()')[0] for d in problem_input.split('do()')]
    for do_string in do_strings:
        total += part1(do_string)
    return total
