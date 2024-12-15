from collections import Counter
from numpy import array, prod, sign, var


def parse_input(file_handle) -> tuple[array,array]:
    positions = []
    velocities = []
    for p,v in (l.split(' ') for l in file_handle.readlines()):
        positions.append(p.split('=')[1].split(','))
        velocities.append(v.split('=')[1].split(','))
    return array(positions, dtype='int64'), array(velocities, dtype='int64')


def part1(problem_input:tuple[array,array]) -> int:
    ps,vs = problem_input
    m = array([101,103], dtype='int64')
    return prod([
        v for k,v in 
        Counter(tuple(p) for p in sign((ps+100*vs)%m-m//2)).items()
        if prod(k)!=0
    ])


def part2(problem_input:tuple[array,array]) -> int:
    ps,vs = problem_input
    m = array([101,103], dtype='int64')
    return min((prod(var((ps+i*vs)%m)), i) for i in range(prod(m)))[1]
