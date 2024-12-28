import subprocess
import sys

from collections import defaultdict

import z3

from solution import Gate, AND, OR, XOR


NODE_SHAPES = {
    AND: ' [shape=ellipse]',
    OR: ' [shape=rect]',
    XOR: ' [shape=octagon]',
}


def graph_circuit(gates:list[Gate], variables:dict[z3.BoolRef,bool], filename:str):
    dot = []
    dot.append('digraph adder {')
    dot.append('rankdir = LR;')
    dot.append('ranksep = 1;')
    
    gates_:set[Gate] = set(gates)
    outputs:dict[z3.BoolRef,Gate|z3.BoolRef] = {}
    inputs:dict[z3.BoolRef,set[Gate|z3.BoolRef]] = defaultdict(set)
    
    for gate in gates_:
        outputs[gate.output] = gate
        inputs[gate.inputA].add(gate)
        inputs[gate.inputB].add(gate)
    
    xynodes_:set[z3.BoolRef] = set()
    znodes_:set[z3.BoolRef] = set()
    for gate in gates_:
        if str(gate.inputA).startswith('x') or str(gate.inputA).startswith('y'):
            xynodes_.add(gate.inputA)
            outputs[gate.inputA] = gate.inputA
            inputs[gate.inputA].add(gate)
        if str(gate.inputB).startswith('x') or str(gate.inputB).startswith('y'):
            xynodes_.add(gate.inputB)
            outputs[gate.inputB] = gate.inputB
            inputs[gate.inputB].add(gate)
        if str(gate.output).startswith('z'):
            znodes_.add(gate.output)
            outputs[gate.output] = gate
            inputs[gate.output].add(gate.output)
    xynodes = sorted(xynodes_, key=lambda x: str(x)[1:]+str(x)[0])
    znodes = sorted(znodes_, key=lambda x: str(x)[1:]+str(x)[0])
    
    dot.append(f'{{rank=same; {"; ".join(str(n)+"[shape=plaintext]" for n in xynodes)}}}')
    dot.append(f'{{{" -> ".join(str(n) for n in xynodes)} [style=invis]}}')
    dot.append(f'{{rank=same; {"; ".join(str(n)+"[shape=plaintext]" for n in znodes)}}}')
    dot.append(f'{{{" -> ".join(str(n) for n in znodes)} [style=invis]}}')
    
    
    found = set()
    for gate in gates_:
        if str(gate.inputA).startswith('x') or str(gate.inputA).startswith('y') or \
           str(gate.inputB).startswith('x') or str(gate.inputB).startswith('y'):
            found.add(gate)
    dot.append(f'{{rank=same; {"; ".join(str(g)+NODE_SHAPES[type(g)] for g in found)}}}')
    
    gates_ -= found
    found = set()
    for gate in gates_:
        if str(gate.output).startswith('z'):
            found.add(gate)
    dot.append(f'{{rank=same; {"; ".join(str(g)+NODE_SHAPES[type(g)] for g in found)}}}')
    
    for t in [AND,OR,XOR,object]:
        gates_ -= found
        found = set()
        for gate in gates_:
            if isinstance(gate, t):
                found.add(gate)
        dot.append(f'{{rank=same; {"; ".join(str(g)+NODE_SHAPES[type(g)] for g in found)}}}')
    
    gates_ -= found
    assert(not gates_)
    
    for outp,g1 in outputs.items():
        for g2 in inputs[outp]:
            dot.append(f'{g1} -> {g2}')
    dot.append('}')
    
    #print('\n'.join(dot), file=sys.stderr)
    with open(filename, 'w') as fh:
        process = subprocess.Popen(['dot', '-T', 'pdf'], stdin=subprocess.PIPE, stdout=fh)
        process.communicate('\n'.join(dot).encode())
