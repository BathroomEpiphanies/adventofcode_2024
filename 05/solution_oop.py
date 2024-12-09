from typing import Self

from collections import defaultdict


class Page:
    
    rules:dict[int,list[int]]
    page:int
    
    def __init__(self, page:int) -> None:
        self.page = page
    
    def __str__(self) -> str:
        return str(self.page)
    
    def __lt__(self, other:Self) -> bool:
        return self.page in self.rules and other.page in self.rules[self.page]
    
    def __int__(self) -> int:
        return self.page


def parse_input(file_handle) -> list[list[Page]]:
    lines = (l.strip() for l in file_handle.readlines())
    
    rules = defaultdict(list)
    for line in lines:
        if line=='':
            break
        a,b = line.split('|')
        rules[int(a)].append(int(b))
    __Page = type("Page", (Page,), {'rules': dict(rules)})
    
    manuals:list[list[Page]] = []
    for line in lines:
        manuals.append([__Page(int(a)) for a in line.split(',')])
    
    return manuals


def part1(problem_input:list[list[Page]]) -> int:
    total:int = 0
    for manual in problem_input:
        manual_ = sorted(manual)
        if manual_ == manual:
            total += int(manual[len(manual)//2])
    return total


def part2(problem_input:list[list[Page]]) -> int:
    total:int = 0
    for manual in problem_input:
        manual_ = sorted(manual)
        if manual_ != manual:
            total += int(manual_[len(manual)//2])
    return total
