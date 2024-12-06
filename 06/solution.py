from collections import defaultdict


def parse_input(file_handle) -> tuple[dict[complex,str],complex,complex]:
    global maxr, maxc
    area:dict[complex,str] = {}
    for r,row in enumerate(file_handle.readlines()):
        for c,a in enumerate(row):
            if a=='^':
                position = c+r*1j
            if a=='#':
                area[c+r*1j] = '#'
            else:
                area[c+r*1j] = '.'
    return area,position,-1j


def distance_until_exit(area:dict[complex,str], position:complex, direction:complex) -> None|int:
    visited:defaultdict[complex,set[complex]] = defaultdict(set)
    while position in area:
        if direction in visited[position]:
            return None
        visited[position].add(direction)
        position_ = position+direction
        if area.get(position_) == '#':
            direction *= 1j
        else:
            position = position_
    return len(visited)


def part1(problem_input:tuple[dict[complex,str],complex,complex]) -> None|int:
    area,position,direction = problem_input
    return distance_until_exit(area, position, direction)


def count_blockers(area:dict[complex,str], position:complex, direction:complex) -> int:
    visited:defaultdict[complex,set[complex]] = defaultdict(set)
    blockers:set[complex] = set()
    while position in area:
        position_ = position+direction
        if area.get(position_)=='.' and position_ not in visited and position_ not in blockers:
            area[position_] = '#'
            if distance_until_exit(area, position, direction) is None:
                blockers.add(position_)
            area[position_] = '.'
        visited[position].add(direction)
        if area.get(position_) == '#':
            direction *= 1j
        else:
            position = position_
    return len(blockers)


def part2(problem_input:tuple[dict[complex,str],complex,complex]) -> int:
    area,position,direction = problem_input
    return count_blockers(area, position, direction)
