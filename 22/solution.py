from collections import Counter
from more_itertools import windowed

import numpy as np


def parse_input(file_handle) -> list[int]:
    return [int(l.strip()) for l in file_handle.readlines()]


def advance_secret_numbers(secret_numbers):
    secret_numbers = (secret_numbers^(secret_numbers<< 6))&0xffffff
    secret_numbers = (secret_numbers^(secret_numbers>> 5))&0xffffff
    secret_numbers = (secret_numbers^(secret_numbers<<11))&0xffffff
    return secret_numbers


def part1(problem_input:list[int]) -> int:
    secret_numbers = np.array(problem_input, dtype='int64')
    for _ in range(2000):
        secret_numbers = advance_secret_numbers(secret_numbers)
    return sum(secret_numbers)


def part2(problem_input:list[int]) -> int:
    secret_number_table = np.ndarray((2001,len(problem_input)), dtype='O')
    secret_numbers = np.array(problem_input, dtype='O')
    for iteration in range(2001):
        secret_number_table[iteration] = secret_numbers
        secret_numbers = advance_secret_numbers(secret_numbers)
    secret_number_table = secret_number_table.T
    price_table = secret_number_table%10
    diff_table = price_table[:,1:]-price_table[:,:-1]
    counter = Counter()
    for diffs,prices in zip(diff_table, price_table):
        found_sequences = set()
        for sequence,price in zip(windowed(diffs, n=4), prices[4:]):
            if sequence not in found_sequences:
                found_sequences.add(sequence)
                counter[sequence] += price
    return counter.most_common(1)[0][1]
