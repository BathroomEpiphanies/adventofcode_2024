from collections import deque


def parse_input(file_handle) -> dict[complex,int]:
    topography:dict[complex,int] = {}
    for r,row in enumerate(l.strip() for l in file_handle.readlines()):
        for c,g in enumerate(row):
            topography[c+r*1j] = int(g)
    return topography


def find_trails(topography, head):
    count = 0
    visited = set()
    queue = deque([head])
    visited.add(head)
    while queue:
        position = queue.pop()
        visited.add(position)
        if topography[position]==9:
            count += 1
            continue
        for direction in [1,1j,-1,-1j]:
            position_ = position+direction
            if position_ in topography and position_ not in visited and topography[position_]==topography[position]+1:
                queue.append(position_)
    return count


def part1(problem_input:dict[complex,int]) -> int:
    trail_heads = [position for position,height in problem_input.items() if height==0]
    return sum(find_trails(problem_input, head) for head in trail_heads)


def part2(problem_input:dict[complex,int]) -> int:
    total:int = 0
    return total
