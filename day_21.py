from typing import Sequence, List, Set

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


with open('day_21.input', 'r') as f:
    data = f.read().split('\n')

instruction_ptr_register = int(data[0].split()[-1])
instructions = []
for line in data[1:]:
    action = line
    func, a, b, c = map(eval, action.split())
    instructions.append((func, a, b, c))

def process(i):
    registers = [0] * 6
    registers[0] = i
    instruction_ptr = 0
    breaks: Set[int] = set()
    try:
        with open('tmp', 'w') as f:
            while True:
                instruction_ptr = registers[instruction_ptr_register]
                f.write(str((instruction_ptr, instructions[instruction_ptr], registers)))
                f.write('\n')
                # So we know that instruction 29 is special, as its the only one that interacts with register 0
                # and register zero is the only one we can manipulate.
                if instruction_ptr == 28:
                    print(registers[2])
                    break
                breaks.add(tuple(registers))
                func, a, b, c = instructions[instruction_ptr]
                registers = func(registers, a, b, c)
                registers[instruction_ptr_register] += 1
    except IndexError:
        print(registers)
# Part 1
process(0)

# Part 2

def run_activation_system(n):
    seen = set()
    c = 0
    last_unique_c = -1

    while True:
        a = c | 65536 
        c = n 
        while True:
            c = (((c + (a & 255)) & 16777215) * 65899) & 16777215
            if 256 > a:
                if c not in seen:
                    seen.add(c)
                    last_unique_c = c
                    break
                else:
                    return last_unique_c
            else:
                a //= 256


n = instructions[7][1] # The loop input, pulled from the 8th instruction.
print(n)
print(run_activation_system(n))