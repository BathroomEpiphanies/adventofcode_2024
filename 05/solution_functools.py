from functools import cmp_to_key, partial


def parse_input(file_handle) -> tuple[dict[int,list[int]], list[list[int]]]:
    rules:dict[int,list[int]] = {}
    manuals:list[list[int]] = []
    lines = (l.strip() for l in file_handle.readlines())
    for line in lines:
        if not line:
            break
        a,b = (int(a) for a in line.split('|'))
        if a not in rules:
            rules[a] = []
        rules[a].append(int(b))
    for line in lines:
        manuals.append([int(a) for a in line.split(',')])
    return rules,manuals


def ordering(a:int, b:int, rules:dict[int,list[int]]) -> int:
    return -1 if a in rules and b in rules[a] else +1


def part1(problem_input:tuple[dict[int,list[int]], list[list[int]]]) -> int:
    rules,manuals = problem_input
    key_function = cmp_to_key(partial(ordering, rules=rules))
    total:int = 0
    for manual in manuals:
        manual_ = sorted(manual, key=key_function)
        if manual == manual_:
            total += manual[len(manual)//2]
    return total


def part2(problem_input:tuple[dict[int,list[int]], list[list[int]]]) -> int:
    rules,manuals = problem_input
    key_function = cmp_to_key(partial(ordering, rules=rules))
    total:int = 0
    for manual in manuals:
        manual_ = sorted(manual, key=key_function)
        if manual != manual_:
            total += manual_[len(manual)//2]
    return total
