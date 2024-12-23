from collections import defaultdict
from functools import cache
from itertools import product
from more_itertools import windowed

from networkx import DiGraph, all_shortest_paths


def parse_input(file_handle) -> list[str]:
    return [l.strip() for l in file_handle.readlines()]


class KeyPad:
    
    _keypad:list[str]
    _paths:dict[str,dict[str,list[str]]]
    
    @staticmethod
    def generate_paths(__keypad:list[str]) -> dict[str,dict[str,list[str]]]:
        graph = DiGraph()
        paths:dict[str,dict[str,list[str]]] = defaultdict(lambda: defaultdict(list))
        for k1,k2 in (keys for row in __keypad for keys in windowed(row, n=2) if all(k!=' ' for k in keys)):
            graph.add_edge(k1, k2, direction='>')
            graph.add_edge(k2, k1, direction='<')
        for k1,k2 in (keys for col in zip(*__keypad) for keys in windowed(col, n=2) if all(k!=' ' for k in keys)):
            graph.add_edge(k1, k2, direction='v')
            graph.add_edge(k2, k1, direction='^')
        for n1,n2 in product(graph.nodes(), repeat=2):
            for path in all_shortest_paths(graph, n1, n2):
                if len(path)>1:
                    keys = [graph[_n1][_n2]['direction'] for _n1,_n2 in windowed(path, n=2)]
                else:
                    keys = []
                paths[n1][n2].append(''.join(keys))
        return paths
    
    @classmethod
    @cache
    def shortest_key_sequence(cls, code, depth):
        if depth==0:
            return code
        sequence = ''
        for a,b in windowed('A'+code, n=2):
            min_path = (float('inf'),'')
            for path in cls._paths[a][b]:
                path_sequence = Directional.shortest_key_sequence(path+'A', depth-1)
                min_path = min(min_path, (len(path_sequence), path_sequence))
            sequence += min_path[1]
        return sequence
    
    @classmethod
    @cache
    def shortest_key_sequence_length(cls, code, depth):
        if depth==0:
            return len(code)
        sequence_length = 0
        for a,b in windowed('A'+code, n=2):
            min_length = float('inf')
            for path in cls._paths[a][b]:
                path_sequence_length = Directional.shortest_key_sequence_length(path+'A', depth-1)
                min_length = min(min_length, path_sequence_length)
            sequence_length += min_length
        return sequence_length


class Numerical(KeyPad):
    _keypad = [
        '789',
        '456',
        '123',
        ' 0A',
    ]
    _paths = KeyPad.generate_paths(_keypad)


class Directional(KeyPad):
    _keypad = [
        ' ^A',
        '<v>',
    ]
    _paths = KeyPad.generate_paths(_keypad)


def part1(problem_input:list[str]) -> int:
    total:int = 0
    for code in problem_input:
        val = int(code[:-1])
        sequence = Numerical.shortest_key_sequence(code, 3)
        print(sequence)
        total += val*len(sequence)
    return total


def part2(problem_input:list[str]) -> int:
    total:int = 0
    for code in problem_input:
        val = int(code[:-1])
        length = Numerical.shortest_key_sequence_length(code, 26)
        total += val*length
    return total
