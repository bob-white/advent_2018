"""--- Day 16: Chronal Classification ---

As you see the Elves defend their hot chocolate successfully, you go back to falling through time. This is going to become a problem.

If you're ever going to return to your own time, you need to understand how this device on your wrist works. You have a little while before you reach your next destination, and with a bit of trial and error, you manage to pull up a programming manual on the device's tiny screen.

According to the manual, the device has four registers (numbered 0 through 3) that can be manipulated by instructions containing one of 16 opcodes. The registers start with the value 0.

Every instruction consists of four values: an opcode, two inputs (named A and B), and an output (named C), in that order. The opcode specifies the behavior of the instruction and how the inputs are interpreted. The output, C, is always treated as a register.

In the opcode descriptions below, if something says "value A", it means to take the number given as A literally. (This is also called an "immediate" value.) If something says "register A", it means to use the number given as A to read from (or write to) the register with that number. So, if the opcode addi adds register A and value B, storing the result in register C, and the instruction addi 0 7 3 is encountered, it would add 7 to the value contained by register 0 and store the sum in register 3, never modifying registers 0, 1, or 2 in the process.

Many opcodes are similar except for how they interpret their arguments. The opcodes fall into seven general categories:

Addition:

    addr (add register) stores into register C the result of adding register A and register B.
    addi (add immediate) stores into register C the result of adding register A and value B.

Multiplication:

    mulr (multiply register) stores into register C the result of multiplying register A and register B.
    muli (multiply immediate) stores into register C the result of multiplying register A and value B.

Bitwise AND:

    banr (bitwise AND register) stores into register C the result of the bitwise AND of register A and register B.
    bani (bitwise AND immediate) stores into register C the result of the bitwise AND of register A and value B.

Bitwise OR:

    borr (bitwise OR register) stores into register C the result of the bitwise OR of register A and register B.
    bori (bitwise OR immediate) stores into register C the result of the bitwise OR of register A and value B.

Assignment:

    setr (set register) copies the contents of register A into register C. (Input B is ignored.)
    seti (set immediate) stores value A into register C. (Input B is ignored.)

Greater-than testing:

    gtir (greater-than immediate/register) sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0.
    gtri (greater-than register/immediate) sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0.
    gtrr (greater-than register/register) sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0.

Equality testing:

    eqir (equal immediate/register) sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0.
    eqri (equal register/immediate) sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0.
    eqrr (equal register/register) sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0.

Unfortunately, while the manual gives the name of each opcode, it doesn't seem to indicate the number. However, you can monitor the CPU to see the contents of the registers before and after instructions are executed to try to work them out. Each opcode has a number from 0 through 15, but the manual doesn't say which is which. For example, suppose you capture the following sample:

Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]

This sample shows the effect of the instruction 9 2 1 2 on the registers. Before the instruction is executed, register 0 has value 3, register 1 has value 2, and registers 2 and 3 have value 1. After the instruction is executed, register 2's value becomes 2.

The instruction itself, 9 2 1 2, means that opcode 9 was executed with A=2, B=1, and C=2. Opcode 9 could be any of the 16 opcodes listed above, but only three of them behave in a way that would cause the result shown in the sample:

    Opcode 9 could be mulr: register 2 (which has a value of 1) times register 1 (which has a value of 2) produces 2, which matches the value stored in the output register, register 2.
    Opcode 9 could be addi: register 2 (which has a value of 1) plus value 1 produces 2, which matches the value stored in the output register, register 2.
    Opcode 9 could be seti: value 2 matches the value stored in the output register, register 2; the number given for B is irrelevant.

None of the other opcodes produce the result captured in the sample. Because of this, the sample above behaves like three opcodes.

You collect many of these samples (the first section of your puzzle input). The manual also includes a small test program (the second section of your puzzle input) - you can ignore it for now.

Ignoring the opcode numbers, how many samples in your puzzle input behave like three or more opcodes?

Your puzzle answer was 624.
--- Part Two ---

Using the samples you collected, work out the number of each opcode and execute the test program (the second section of your puzzle input).

What value is contained in register 0 after executing the test program?

Your puzzle answer was 584.
"""

import re
from collections import defaultdict
from typing import Dict, Callable, Set, List, Tuple, Sequence


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
    result[c] = bool(a > result[b])
    return result

def gtri(regs: Sequence[int], a: int, b: int, c: int) -> List[int]:
    result = list(regs)
    result[c] = bool(result[a] > b)
    return result

def gtrr(regs: Sequence[int], a: int, b: int, c: int) -> List[int]:
    result = list(regs)
    result[c] = bool(result[a] > result[b])
    return result

def eqir(regs: Sequence[int], a: int, b: int, c: int) -> List[int]:
    result = list(regs)
    result[c] = bool(a == result[b])
    return result

def eqri(regs: Sequence[int], a: int, b: int, c: int) -> List[int]:
    result = list(regs)
    result[c] = bool(result[a] == b)
    return result

def eqrr(regs: Sequence[int], a: int, b: int, c: int) -> List[int]:
    result = list(regs)
    result[c] = bool(result[a] == result[b])
    return result


OPERATIONS = [
    addr, 
    addi,
    mulr, 
    muli,
    banr, 
    bani,
    borr, 
    bori,
    setr, 
    seti,
    gtir, 
    gtri, 
    gtrr,
    eqir, 
    eqri, 
    eqrr
]
# Input was broken into two parts, first part describes the opcode tests.
# So all the Before / After text.
# Second part is what is needed for part 2, and those are the operations to run
# once we've figured out which code maps to which function.
with open('day_16.opcodes', 'r') as f:
    data = f.read()

opcodes: Dict[Callable, Set[int]] = defaultdict(set)
test_data = re.findall(r'Before: \[.*\]', data, re.MULTILINE|re.DOTALL)[0].split('\n')
tests = []
for i in range((len(test_data) // 4) + 1):
    tests.append(test_data[i*4:i*4+4])

op_count = 0
for test in tests:
    _before, _data, _after, *_ = test
    before = tuple(map(int, re.findall(r'\d+', _before)))
    op_data = tuple(map(int, re.findall(r'\d+', _data)))
    after = list(map(int, re.findall(r'\d+', _after)))
    opcode, a, b, c = op_data
    count = 0
    for op in OPERATIONS:
        if op(before, a, b, c) == after:
            count += 1
            opcodes[op].add(opcode)
    if count >= 3:
        op_count +=1
# Part 1
print(op_count)

# Mapping each opcode number to a function.
# Each function maps to exactly 1 opcode number, and luckily
# if you inspect the data at this point, one of those functions maps to just one code
# so we'll find the function that maps to the least number of codes, then remove that code from
# all the other functions, as we keep processing them like this, we should get a clean 1-1 mapping.
# A more complex overlap would probably call for doing something fancy with set intersections, and
# it is posslbe that other inputs lead to that problem.
code_to_func: Dict[int, Callable] = {}
while any(codes for codes in opcodes.values()):
    op = min(opcodes, key=lambda x: len(opcodes[x]))
    codes = opcodes.pop(op)
    code = codes.pop()
    code_to_func[code] = op
    for val in opcodes.values():
        val.discard(code)

# This should ensure that we've actually mapped every opcode to a function.
assert len(code_to_func) == 16

with open('day_16.input', 'r') as f:
    data = f.read()

operations: List[List[int]] = [list(map(int, line.split(' '))) for line in data.split('\n') if line]

registers = [0, 0, 0, 0]
for opc, a, b, c in operations:
    registers = code_to_func[opc](registers, a, b, c)

# Part 2
print(registers[0])
