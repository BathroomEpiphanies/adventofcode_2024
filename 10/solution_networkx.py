import networkx as nx
from itertools import product
from more_itertools import ilen


def parse_input(file_handle) -> nx.DiGraph:
    graph:nx.DiGraph = nx.DiGraph()
    topography:dict[complex,int] = {}
    for r,row in enumerate(l.strip() for l in file_handle.readlines()):
        for c,height in enumerate(row):
            topography[c+r*1j] = int(height)
    for position,height in topography.items():
        if height==0:
            graph.add_edge('source', position)
        if height==9:
            graph.add_edge(position, 'sink')
        for d in [1,1j,-1,-1j]:
            n = position+d
            if n in topography and topography[n]==height+1:
                graph.add_edge(position, n)
    return graph


def part1(problem_input:nx.DiGraph) -> int:
    trail_heads = [node for node in problem_input['source']]
    trail_tails = [edge[0] for edge in problem_input.edges() if edge[1]=='sink']
    paths = dict(nx.all_pairs_shortest_path(problem_input))
    # Potentially useful in later versions of networkx
    # paths = dict(nx.single_source_all_shortest_paths(problem_input, 'source'))
    return ilen(tail for head,tail in product(trail_heads, trail_tails) if tail in paths[head])


def part2(problem_input:nx.DiGraph) -> int:
    return ilen(nx.all_simple_paths(problem_input, 'source', 'sink'))
