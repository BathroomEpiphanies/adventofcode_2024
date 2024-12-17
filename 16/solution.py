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
        for d in directions[:2]:
            if p+d in __maze:
                maze.add_edge(Node(p,d), Node(p+d,d), weight=1)
    maze.add_edge(source, Node(start,1), weight=0)
    for d in directions:
        maze.add_edge(Node(end,d), sink, weight=0)
    return maze, source, sink


def part1(problem_input:tuple[nx.Graph, Node, Node]) -> int:
    maze,source,sink = problem_input
    return nx.shortest_path_length(maze, source, sink, weight='weight')


def part2(problem_input:tuple[nx.Graph, Node, Node]) -> int:
    maze,source,sink = problem_input
    good_tiles:set[complex] = set()
    for path in nx.all_shortest_paths(maze, source, sink, weight="weight"):
        good_tiles |= {n.position for n in path[1:-1]}
    return len(good_tiles)
