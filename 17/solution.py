

class Computer:
    A:int
    B:int
    C:int
    program:list[int]
    pointer:int
    output:list[int]
    
    def __init__(self, registers:tuple[int,int,int], program:list[int]) -> None:
        self.A,self.B,self.C = registers
        self.program = program
    
    def __str__(self) -> str:
        return f'({self.A},{self.B},{self.C}): {",".join(str(i) for i in self.output)}'
    
    def get_combo(self, combo:int) -> int:
        if combo<4:    return combo
        elif combo==4: return self.A
        elif combo==5: return self.B
        elif combo==6: return self.C
        else: raise KeyError
    
    def adv(self, combo:int) -> None:
        self.A = self.A // 2**self.get_combo(combo)
        self.pointer += 2
    
    def bxl(self, literal:int) -> None:
        self.B = self.B ^ literal
        self.pointer += 2
    
    def bst(self, combo:int) -> None:
        self.B = self.get_combo(combo)%8
        self.pointer += 2
    
    def jnz(self, literal:int) -> None:
        if self.A==0:
            self.pointer += 2
        else:
            self.pointer = literal
    
    def bxc(self, _):
        self.B = self.B ^ self.C
        self.pointer += 2
    
    def out(self, combo:int) -> None:
        self.output.append(self.get_combo(combo)%8)
        self.pointer += 2
    
    def bdv(self, combo:int) -> None:
        self.B = self.A // 2**self.get_combo(combo)
        self.pointer += 2
    
    def cdv(self, combo:int) -> None:
        self.C = self.A // 2**self.get_combo(combo)
        self.pointer += 2
    
    def run(self) -> None:
        self.pointer = 0
        self.output = []
        while self.pointer < len(self.program):
            {
                0: self.adv,
                1: self.bxl,
                2: self.bst,
                3: self.jnz,
                4: self.bxc,
                5: self.out,
                6: self.bdv,
                7: self.cdv,
            }[self.program[self.pointer]](self.program[self.pointer+1])


def parse_input(file_handle) -> Computer:
    lines = [l.strip() for l in file_handle.readlines()]
    A = int(lines[0].split(': ')[-1])
    B = int(lines[1].split(': ')[-1])
    C = int(lines[2].split(': ')[-1])
    program = [int(i) for i in lines[4].split(': ')[-1].split(',')]
    return Computer((A,B,C),program)


def part1(problem_input:Computer) -> str:
    problem_input.run()
    return str(problem_input)


def part2(problem_input:Computer) -> str:
    computer = problem_input
    A = [0]*len(computer.program)
    
    def __find_computer(n=0):
        for i in range(8):
            A[n] = i
            A_ = sum(a*8**p for p,a in enumerate(reversed(A)))
            computer.A = A_
            computer.run()
            if computer.output[-n-1:] != computer.program[-n-1:]:
                continue
            if n==len(A)-1:
                computer.A = A_
                return computer
            if _ := __find_computer(n+1):
                return _
    
    return str(__find_computer())
