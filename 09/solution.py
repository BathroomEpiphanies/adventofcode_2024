from dataclasses import dataclass
from itertools import accumulate, count, cycle


@dataclass
class Segment:
    number:int
    position:int
    length:int


def parse_input(file_handle) -> list[Segment]:
    lengths = [int(a) for a in file_handle.readline().strip()]
    numbers = (next(it) for it in cycle([count(0,1), count(-1,-1)]))
    positions = accumulate(lengths, initial=0)
    return [
        Segment(number, position, length) for
        number,position,length in zip(numbers, positions, lengths)
    ]


def part1(problem_input:list[Segment]) -> int:
    memory = []
    for segment in problem_input:
        memory.extend([segment.number]*segment.length)
    head = 0
    tail = len(memory)-1
    while head<tail:
        while memory[head]>=0:
            head += 1
        while memory[tail]<0:
            tail -= 1
        if head>=tail:
            break
        memory[head],memory[tail] = memory[tail],memory[head]
    return sum(a*b for a,b in zip(count(),memory) if b>=0)


def part2(problem_input:list[Segment]) -> int:
    files = problem_input[::2]
    gaps = problem_input[1::2]
    for file_ in reversed(files):
        for gap in gaps:
            if gap.position>file_.position:
                continue
            if file_.length<=gap.length:
                file_.position = gap.position
                gap.position += file_.length
                gap.length -= file_.length
    
    def _checksum(f:Segment):
        return f.number*f.length*(f.position+f.position+f.length-1)//2
    
    return sum(_checksum(f) for f in files)
