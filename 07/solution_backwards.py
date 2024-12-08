from typing import Callable


def parse_input(file_handle) -> list[tuple[int,list[int]]]:
    equations = []
    for line in (l.strip() for l in file_handle.readlines()):
        result,operands = line.split(': ')
        equations.append((int(result),[int(o) for o in operands.split(' ')]))
    return equations


def unadd(result:int, operand:int) -> int:
    if result<operand:
        raise ArithmeticError
    return result-operand


def unmul(result:int, operand:int) -> int:
    if result%operand!=0:
        raise ArithmeticError
    return result//operand


def unconcat(result:int, operand:int) -> int:
    operand_ = str(operand)
    result_ = str(result)
    remainder_ = result_.removesuffix(operand_)
    if remainder_=='' or remainder_==result_:
        raise ArithmeticError
    return int(remainder_)


def satisfiable(
    result:int,
    operands:list[int],
    operations:list[Callable[[int,int],int]],
) -> bool:
    *operands,operand = operands
    if not operands:
        return result==operand
    for operation in operations:
        try:
            if satisfiable(operation(result, operand), operands, operations):
                return True
        except ArithmeticError:
            continue
    return False


def part1(problem_input:list[tuple[int,list[int]]]) -> int:
    return sum(result for result,operands in problem_input if satisfiable(result, operands, [unmul,unadd]))


def part2(problem_input:list[tuple[int,list[int]]]) -> int:
    return sum(result for result,operands in problem_input if satisfiable(result, operands, [unconcat,unmul,unadd]))
