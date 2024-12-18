from itertools import product

import networkx as nx


def parse_input(file_handle) -> list[tuple[int,int]]:
    return [(int(a),int(b)) for a,b in (l.strip().split(',') for l in file_handle.readlines())]


def distance_to_target_at_time(
    memory_size:int,
    corruptions:list[tuple[int,int]],
    time:int
) -> int:
    origin = (0,0)
    target = (memory_size-1,memory_size-1)
    memory = nx.Graph()
    for a,b in product(range(memory_size), repeat=2):
        memory.add_edge((a,b), (a+1,b))
        memory.add_edge((a,b), (a,b+1))
    for c in corruptions[:time]:
        memory.remove_node(c)
    return nx.shortest_path_length(memory, origin, target)


def part1(problem_input:list[tuple[int,int]]) -> int:
    corruptions = problem_input
    corruption_time = 1024 if len(corruptions)>100 else 12
    memory_size = 71 if len(corruptions)>100 else 7
    return distance_to_target_at_time(memory_size, corruptions, corruption_time)


def part2(problem_input:list[tuple[int,int]]) -> str:
    corruptions = problem_input
    memory_size = 71 if len(corruptions)>100 else 7
    lower_bound,upper_bound = 0,len(corruptions)
    while upper_bound>lower_bound:
        middle = (lower_bound+upper_bound)//2+1
        try:
            distance_to_target_at_time(memory_size, corruptions, middle)
            lower_bound = middle
        except nx.exception.NetworkXNoPath:
            upper_bound = middle-1
    return f'{corruptions[lower_bound][0]},{corruptions[lower_bound][1]}'
