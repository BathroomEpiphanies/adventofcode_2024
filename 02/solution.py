from typing import Generator


def parse_input(file_handle) -> list[list[int]]:
    return [[int(a) for a in l.split()] for l in file_handle.readlines()]


def report_is_safe(report:list[int]) -> bool:
    return all(0<b-a<4 for a,b in zip(report[:-1], report[1:])) or \
           all(0<b-a<4 for b,a in zip(report[:-1], report[1:]))


def part1(problem_input:list[list[int]]) -> int:
    sum:int = 0
    for report in problem_input:
        if report_is_safe(report):
            sum += 1
    return sum


def dampened_reports(report:list[int]) -> Generator[list[int], None, None]:
    for position in range(len(report)):
        yield report[:position]+report[position+1:]


def part2(problem_input:list[list[int]]) -> int:
    sum:int = 0
    for report in problem_input:
        if any(report_is_safe(r) for r in dampened_reports(report)):
            sum += 1
    return sum
