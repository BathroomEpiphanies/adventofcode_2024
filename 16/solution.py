import networkx as nx
from typing import NamedTuple


class Node(NamedTuple):
    position:complex
    heading:complex


def parse_input(file_handle) -> tuple[nx.Graph, Node, Node]:
    directions = [1,-1j,-1,1j]
    start:complex = 0
    end:complex = 0
    __maze:set[complex] = set()
    for r,row in enumerate(l.strip() for l in file_handle.readlines()):
        for c,m in enumerate(row):
            if m=='#':
                continue
            __maze.add(c+r*1j)
            if m=='S':
                start = c+r*1j
            if m=='E':
                end = c+r*1j
    maze = nx.Graph()
    source = Node(-1, 0)
    sink = Node(-2, 0)
    for p in __maze:
        for d1,d2 in zip(directions, (1j*d for d in directions)):
            maze.add_edge(Node(p,d1), Node(p,d2), weight=1000)
        for d in directions:
            if p+d in __maze:
                maze.add_edge(Node(p,d), Node(p+d,d), weight=1)
    maze.add_edge(source, Node(start,1), weight=0)
    for d in directions:
        maze.add_edge(Node(end,d), sink, weight=0)
    return maze, source, sink


def part1(problem_input:tuple[nx.Graph, Node, Node]) -> int:
    maze,source,sink = problem_input
    return nx.dijkstra_path_length(maze, source, sink)


def part2(problem_input:tuple[nx.Graph, Node, Node]) -> int:
    maze,source,sink = problem_input
    best_score = part1(problem_input)
    distances:dict[Node,dict[Node,int]] = {
        source: dict(nx.single_source_dijkstra_path_length(maze, source, cutoff=best_score)),
        sink: dict(nx.single_source_dijkstra_path_length(maze, sink, cutoff=best_score)),
    }
    nodes_to_check = distances[source].keys() & distances[sink].keys() - {source, sink}
    good_nodes:set[Node] = set()
    for node in nodes_to_check:
        if distances[source][node] + distances[sink][node] <= distances[source][sink]:
            good_nodes.add(node)
    good_nodes -= {source, sink}
    good_tiles:set[complex] = {n.position for n in good_nodes}
    return len(good_tiles)
