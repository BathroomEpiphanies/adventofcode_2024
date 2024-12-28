from typing import Self

from abc import ABC,abstractmethod

import z3


class Gate(ABC):
    inputA:z3.BoolRef
    inputB:z3.BoolRef
    output:z3.BoolRef
    
    def __init__(self, inputA, inputB, output):
        inputA,inputB = sorted((inputA,inputB))
        self.inputA = z3.Bool(inputA)
        self.inputB = z3.Bool(inputB)
        self.output = z3.Bool(output)
    
    def __hash__(self) -> int:
        return id(self)
    
    def __lt__(self, other:Self) -> bool:
        return (self.inputA, self.inputB, type(self)) < (self.inputA, self.inputB, type(self))
    
    @abstractmethod
    def __str__(self) -> str:
        ...
    
    @abstractmethod
    def eval(self) -> z3.BoolRef:
        ...


class AND(Gate):
    
    def eval(self) -> z3.BoolRef:
        return z3.And(self.inputA, self.inputB) == self.output
    
    def __str__(self) -> str:
        return f'"AND {self.inputA} {self.inputB}: {self.output}"'


class OR(Gate):
    
    def eval(self) -> z3.BoolRef:
        return z3.Or(self.inputA, self.inputB) == self.output
    
    def __str__(self) -> str:
        return f'" OR {self.inputA} {self.inputB}: {self.output}"'


class XOR(Gate):
    
    def eval(self) -> z3.BoolRef:
        return z3.Xor(self.inputA, self.inputB) == self.output
    
    def __str__(self) -> str:
        return f'"XOR {self.inputA} {self.inputB}: {self.output}"'
