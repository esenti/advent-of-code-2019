
from pathlib import Path
from itertools import permutations

def run(instructions, input_buffer, output_buffer):
    i = 0
    while i < len(instructions):
        opcode = instructions[i]
        opcode_str = '{:0>5}'.format(opcode)

        mode1 = opcode_str[2]
        mode2 = opcode_str[1]

        if opcode_str[3:] == '01':
            arg1 = instructions[i + 1]
            arg2 = instructions[i + 2]
            arg3 = instructions[i + 3]
            arg1 = arg1 if mode1 == '1' else instructions[arg1]
            arg2 = arg2 if mode2 == '1' else instructions[arg2]
            instructions[arg3] = arg1 + arg2
            i += 4
        elif opcode_str[3:] == '02':
            arg1 = instructions[i + 1]
            arg2 = instructions[i + 2]
            arg3 = instructions[i + 3]
            arg1 = arg1 if mode1 == '1' else instructions[arg1]
            arg2 = arg2 if mode2 == '1' else instructions[arg2]
            instructions[arg3] = arg1 * arg2
            i += 4
        elif opcode_str[3:] == '03':
            arg1 = instructions[i + 1]
            instructions[arg1] = input_buffer.pop()
            i += 2
        elif opcode_str[3:] == '04':
            arg1 = instructions[i + 1]
            arg1 = arg1 if mode1 == '1' else instructions[arg1]
            output_buffer.append(arg1)
            i += 2
        elif opcode_str[3:] == '05':
            arg1 = instructions[i + 1]
            arg2 = instructions[i + 2]
            arg1 = arg1 if mode1 == '1' else instructions[arg1]
            arg2 = arg2 if mode2 == '1' else instructions[arg2]

            if arg1 != 0:
                i = arg2
            else:
                i += 3
        elif opcode_str[3:] == '06':
            arg1 = instructions[i + 1]
            arg2 = instructions[i + 2]
            arg1 = arg1 if mode1 == '1' else instructions[arg1]
            arg2 = arg2 if mode2 == '1' else instructions[arg2]

            if arg1 == 0:
                i = arg2
            else:
                i += 3
        elif opcode_str[3:] == '07':
            arg1 = instructions[i + 1]
            arg2 = instructions[i + 2]
            arg3 = instructions[i + 3]
            arg1 = arg1 if mode1 == '1' else instructions[arg1]
            arg2 = arg2 if mode2 == '1' else instructions[arg2]

            instructions[arg3] = 1 if arg1 < arg2 else 0
            i += 4
        elif opcode_str[3:] == '08':
            arg1 = instructions[i + 1]
            arg2 = instructions[i + 2]
            arg3 = instructions[i + 3]
            arg1 = arg1 if mode1 == '1' else instructions[arg1]
            arg2 = arg2 if mode2 == '1' else instructions[arg2]

            instructions[arg3] = 1 if arg1 == arg2 else 0
            i += 4
        elif opcode_str[3:] == '99':
            break

if __name__ == '__main__':
    with open(Path(__file__).parent / 'input.txt') as f:
        lines = f.read()

    instructions = [int(x) for x in lines.split(',')]
    outputs = []

    for sequence in permutations(range(5)):
        input_buffer = []
        output_buffer = [0]

        for i in sequence:
            input_buffer = output_buffer
            output_buffer = []

            input_buffer.append(i)
            run(instructions.copy(), input_buffer, output_buffer)

        outputs.append(output_buffer[-1])

    print(max(outputs))
