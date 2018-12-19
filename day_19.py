
from typing import Sequence, List

def addr(regs: Sequence[int], a: int, b: int, c: int) -> List[int]:
    result = list(regs)
    result[c] = result[a] + result[b]
    return result

def addi(regs: Sequence[int], a: int, b: int, c: int) -> List[int]:
    result = list(regs)
    result[c] = result[a] + b
    return result

def mulr(regs: Sequence[int], a: int, b: int, c: int) -> List[int]:
    result = list(regs)
    result[c] = result[a] * result[b]
    return result

def muli(regs: Sequence[int], a: int, b: int, c: int) -> List[int]:
    result = list(regs)
    result[c] = result[a] * b
    return result

def banr(regs: Sequence[int], a: int, b: int, c: int) -> List[int]:
    result = list(regs)
    result[c] = result[a] & result[b]
    return result

def bani(regs: Sequence[int], a: int, b: int, c: int) -> List[int]:
    result = list(regs)
    result[c] = result[a] & b
    return result

def borr(regs: Sequence[int], a: int, b: int, c: int) -> List[int]:
    result = list(regs)
    result[c] = result[a] | result[b]
    return result

def bori(regs: Sequence[int], a: int, b: int, c: int) -> List[int]:
    result = list(regs)
    result[c] = result[a] | b
    return result

def setr(regs: Sequence[int], a: int, b: int, c: int) -> List[int]:
    result = list(regs)
    result[c] = result[a]
    return result

def seti(regs: Sequence[int], a: int, b: int, c: int) -> List[int]:
    result = list(regs)
    result[c] = a
    return result

def gtir(regs: Sequence[int], a: int, b: int, c: int) -> List[int]:
    result = list(regs)
    result[c] = int(a > result[b])
    return result

def gtri(regs: Sequence[int], a: int, b: int, c: int) -> List[int]:
    result = list(regs)
    result[c] = int(result[a] > b)
    return result

def gtrr(regs: Sequence[int], a: int, b: int, c: int) -> List[int]:
    result = list(regs)
    result[c] = int(result[a] > result[b])
    return result

def eqir(regs: Sequence[int], a: int, b: int, c: int) -> List[int]:
    result = list(regs)
    result[c] = int(a == result[b])
    return result

def eqri(regs: Sequence[int], a: int, b: int, c: int) -> List[int]:
    result = list(regs)
    result[c] = int(result[a] == b)
    return result

def eqrr(regs: Sequence[int], a: int, b: int, c: int) -> List[int]:
    result = list(regs)
    result[c] = int(result[a] == result[b])
    return result

data = """
#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5
""".split('\n')[1:-1]

with open('day_19.input', 'r') as f:
    data = f.read().split('\n')

instruction_ptr_register = int(data[0].split()[-1])
instructions = []
for line in data[1:]:
    action = line
    func, a, b, c = map(eval, action.split())
    instructions.append((func, a, b, c))

for i in range(2):
    registers = [0] * 6
    registers[0] = i
    try:
        debug = False
        while True:
            instruction_ptr = registers[instruction_ptr_register]
            # So this is hard coded to my input, I think I can work out a general case though by extracting the storage register
            # from the opcodes.
            # But from watching the values of part 1 I noticed that we were dropping into a pretty deep loop, that appeared to be looking for
            # factors of the value stored in register 5, and once it would find that factor it would add it register 0.
            # Also this loop was kicked off by hitting instructions[1]
            # So once we hit instruction_ptr 1, we can just do the math ourselves.
            # I'm pretty sure that both the storage register, and the loop kickoff ptr might be different based on your input.
            # But I'm not 100% sure. Will need to run some other input through it.
            if instruction_ptr == 1:
                num = registers[5]
                print("Part {}".format(i + 1), sum(x for x in range(1, num + 1) if not num % x))
                break
            func, a, b, c = instructions[instruction_ptr]
            registers = func(registers, a, b, c)
            registers[instruction_ptr_register] += 1
    except IndexError:
        print("Part {}".format(i + 1), registers[0])

