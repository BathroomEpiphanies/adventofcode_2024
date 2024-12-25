from itertools import product

import numpy as np


def parse_input(file_handle) -> tuple[list[np.ndarray],list[np.ndarray]]:
    file_content = file_handle.read().strip()
    locks:list[np.ndarray] = []
    keys:list[np.ndarray] = []
    for file_chunk in file_content.split('\n\n'):
        thing = np.array([list(line) for line in file_chunk.split('\n')]) == '#'
        if thing[0].all():
            keys.append(thing)
        else:
            locks.append(thing)
    return locks, keys


def part1(locks:np.ndarray, keys:np.ndarray) -> int:
    return sum(not (lock&key).any() for lock,key in product(locks, keys))


def part2(*_) -> None:
    return None
