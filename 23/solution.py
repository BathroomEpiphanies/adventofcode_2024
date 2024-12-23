from collections import deque

from networkx import Graph, enumerate_all_cliques


def parse_input(file_handle) -> Graph:
    network = Graph()
    network.add_edges_from(l.strip().split('-') for l in file_handle.readlines())
    return network


def part1(problem_input:Graph) -> int:
    total:int = 0
    for clique in enumerate_all_cliques(problem_input):
        if len(clique)>3:
            break
        if len(clique)==3 and any(n.startswith('t') for n in clique):
            total += 1
    return total


def part2(problem_input:Graph) -> str:
    cliques = deque(enumerate_all_cliques(problem_input), maxlen=1)
    return ','.join(sorted(cliques.popleft()))


# Equivalent to deque in later version of more_itertools
#def part2(problem_input:Graph) -> str:
    #from itertools import tail
    #return ','.join(sorted(tail(1, enumerate_all_cliques(problem_input))))
