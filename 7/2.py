
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
            while not input_buffer:
                yield
            instructions[arg1] = input_buffer.pop(0)
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
    max_output = 0

    for sequence in permutations(range(5, 10)):
        inputs = [[x] for x in sequence]
        outputs = [[] for x in range(5)]

        instruction_sets = [(i, run(instructions.copy(), inputs[i], outputs[i]), inputs[i], outputs[i]) for i in range(5)]

        inputs[0].append(0)
        instructions_to_run = instruction_sets.copy()

        while instructions_to_run:
            i = instructions_to_run.pop(0)

            try:
                i[3].clear()
                next(i[1])
                instructions_to_run.append(i)
            except StopIteration:
                pass

            instruction_sets[(i[0] + 1) % len(instruction_sets)][2].extend(i[3])

        max_output = max(max_output, max((o[-1] for o in outputs)))

    print(max_output)
