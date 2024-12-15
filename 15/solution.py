

def parse_input(file_handle) -> tuple[dict[complex,str],list[complex],complex]:
    warehouse:dict[complex,str] = {}
    position:complex = 0
    lines = (l.strip() for l in file_handle.readlines())
    for r,row in enumerate(lines):
        if not row: break
        for c,w in enumerate(row):
            if w=='@':
                position = c+r*1j
            warehouse[c+r*1j] = w
    moves = [{'>':1,'^':-1j,'<':-1,'v':1j}[m] for l in lines for m in l]
    return warehouse,moves,position


def print_warehouse(warehouse:dict[complex,str]) -> None:
    maxx = round(max(w.real for w in warehouse))+1
    maxy = round(max(w.imag for w in warehouse))+1
    [print(''.join([warehouse[x+y*1j] for x in range(maxx)])) for y in range(maxy)]


def box_gps_total(warehouse:dict[complex,str]) -> int:
    return round(sum(100*p.imag+p.real for p,w in warehouse.items() if w in 'O['))


def find_positions_to_move(
    warehouse:dict[complex,str],
    origin:complex,
    direction:complex,
    found:set[complex]
) -> tuple[bool,set[complex]]:
    if origin in found:
        return True,found
    found.add(origin)
    if warehouse[origin] == '.':
        return True,found
    if warehouse[origin] == '#':
        return False,set()
    if warehouse[origin] in 'O@':
        return find_positions_to_move(warehouse, origin+direction, direction, found)
    if warehouse[origin] in '[]' and direction in [1, -1]:
        return find_positions_to_move(warehouse, origin+direction, direction, found)
    if warehouse[origin] == '[':
        return (
            find_positions_to_move(warehouse, origin+direction, direction, found)[0] and
            find_positions_to_move(warehouse, origin+1, direction, found)[0]
            ,found
        )
    if warehouse[origin] == ']':
        return (
            find_positions_to_move(warehouse, origin+direction, direction, found)[0] and
            find_positions_to_move(warehouse, origin-1, direction, found)[0]
            ,found
        )
    return False,set()


def move_positions(
    warehouse:dict[complex,str],
    positions:set[complex],
    direction:complex
) -> None:
    updates:dict[complex,str] = {p:'.' for p in positions}
    for tile in positions:
        if warehouse[tile]=='.':
            continue
        updates[tile+direction] = warehouse[tile]
    warehouse |= updates


def part1(problem_input:tuple[dict[complex,str],list[complex],complex]) -> int:
    warehouse,moves,position = problem_input
    for direction in moves:
        can_move,to_move = find_positions_to_move(warehouse, position, direction, set())
        if can_move:
            move_positions(warehouse, to_move, direction)
            position += direction
    print_warehouse(warehouse)
    return box_gps_total(warehouse)


def part2(problem_input:tuple[dict[complex,str],list[complex],complex]) -> int:
    warehouse,moves,position = problem_input
    warehouse_:dict[complex,str] = {}
    for p,w in warehouse.items():
        if w=='O':
            warehouse_[p.real*2+p.imag*1j  ] = '['
            warehouse_[p.real*2+p.imag*1j+1] = ']'
        elif w=='@':
            warehouse_[p.real*2+p.imag*1j  ] = '@'
            warehouse_[p.real*2+p.imag*1j+1] = '.'
        else:
            warehouse_[p.real*2+p.imag*1j  ] = w
            warehouse_[p.real*2+p.imag*1j+1] = w
    position_ = position.real*2+position.imag*1j
    return part1((warehouse_,moves,position_))
