import sys

import z3

from gates import Gate, AND, OR, XOR
from graph_circuit import graph_circuit


def parse_input(file_handle) -> tuple[list[Gate], dict[z3.BoolRef,bool]]:
    value_lines, gate_lines = file_handle.read().strip().split('\n\n')
    values:dict[z3.BoolRef,bool] = {}
    gates:list[Gate] = []
    for line in value_lines.split('\n'):
        var,val = line.split(': ')
        values[z3.Bool(var)] = bool(int(val))
    for line in gate_lines.split('\n'):
        gate,output = line.split(' -> ')
        inputA,operation,inputB = tuple(gate.split(' '))
        if operation=='AND':
            gates.append( AND(inputA, inputB, output) )
        if operation=='OR':
            gates.append( OR(inputA, inputB, output) )
        if operation=='XOR':
            gates.append( XOR(inputA, inputB, output) )
    return gates,values


def find_model(gates:list[Gate], variables:dict[z3.BoolRef,bool]) -> z3.ModelRef:
    solver:z3.Solver = z3.Solver()
    for variable,value in variables.items():
        solver.append(variable==value)
    for gate in gates:
        solver.append(gate.eval())
    solver.check()
    model = solver.model()
    return model


def get_variable_value(model:z3.ModelRef, variable:str) -> int:
    return sum(z3.is_true(model[bit]) * 2**int(str(bit)[1:]) for bit in model if str(bit).startswith(variable))


def part1(gates:list[Gate], variables:dict[z3.BoolRef,bool]) -> int:
    model = find_model(gates, variables)
    return get_variable_value(model, 'z')


def swap_outputs(gates:list[Gate], output1:str, output2:str):
    try:
        gate1 = next(g for g in gates if str(g.output)==output1)
        gate2 = next(g for g in gates if str(g.output)==output2)
        gate1.output,gate2.output = gate2.output,gate1.output
    except StopIteration as e:
        print(f'Outputs: ({output1},{output2}) not in network')


def part2(gates:list[Gate], variables:dict[z3.BoolRef,bool]) -> str:
    graph_circuit(gates, variables, 'before.pdf')
    model = find_model(gates, variables)
    x = get_variable_value(model, 'x')
    print(f'  x={x}: {x:046b}', file=sys.stderr)
    y = get_variable_value(model, 'y')
    print(f'  y={y}: {y:046b}', file=sys.stderr)
    print(f'x+y={x+y}: {x+y:046b}', file=sys.stderr)
    z = get_variable_value(model, 'z')
    print(f'  z={z}: {z:046b}', file=sys.stderr)
    print(f'x+y=z? {x+y==z}', file=sys.stderr)
    
    output_swaps = (
        ('z07', 'shj'),
        ('z23', 'pfn'),
        ('z27', 'kcd'),
        ('tpk', 'wkb'),
    )
    for output1,output2 in output_swaps:
        swap_outputs(gates, output1, output2)
    
    graph_circuit(gates, variables, 'after.pdf')
    model = find_model(gates, variables)
    x = get_variable_value(model, 'x')
    print(f'  x={x}: {x:046b}', file=sys.stderr)
    y = get_variable_value(model, 'y')
    print(f'  y={y}: {y:046b}', file=sys.stderr)
    print(f'x+y={x+y}: {x+y:046b}', file=sys.stderr)
    z = get_variable_value(model, 'z')
    print(f'  z={z}: {z:046b}', file=sys.stderr)
    print(f'x+y=z? {x+y==z}', file=sys.stderr)
    
    if x+y==z:
        return ','.join(sorted(o for os in output_swaps for o in os))
    else:
        return 'Wrong answer'
