from itertools import product

import networkx as nx


def parse_input(file_handle) -> tuple[nx.Graph,complex,complex]:
    __track:set[complex] = set()
    for r,row in enumerate(l.strip() for l in file_handle.readlines()):
        for c,g in enumerate(row):
            if g=='#':
                continue
            position = c+r*1j
            if g=='S':
                start = position
            if g=='E':
                end = position
            __track.add(c+r*1j)
    track = nx.Graph()
    for p,d in product(__track, [1,1j]):
        if p+d in __track:
            track.add_edge(p, p+d)
    return track,start,end


def manhattan_annulus(r1, r2):
    return [
        (dx+dy*1j,abs(dx)+abs(dy)) 
        for dx,dy in product(range(-r2,r2+1), repeat=2)
        if r1<=abs(dx)+abs(dy)<=r2
    ]


def count_cheats(track, end, cheat_length):
    lengths_to_end = dict(nx.single_target_shortest_path_length(track, end))
    offsets = manhattan_annulus(2,cheat_length)
    total = 0
    for position,(offset,distance) in product(lengths_to_end, offsets):
        target = position+offset
        if target in lengths_to_end and \
           lengths_to_end[target]-lengths_to_end[position]-distance>=100:
            total += 1
    return total


def part1(problem_input:tuple[nx.Graph,complex,complex]) -> int:
    track,_,end = problem_input
    return count_cheats(track, end, 2)


def part2(problem_input:tuple[nx.Graph,complex,complex]) -> int:
    track,_,end = problem_input
    return count_cheats(track, end, 20)
