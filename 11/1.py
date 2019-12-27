from pathlib import Path
from collections import defaultdict

def run(instructions, input_buffer, output_buffer):
    i = 0
    relative_base = 0

    def get_arg_value(arg, mode):
        if mode == '0':
            return instructions[arg]
        elif mode == '1':
            return arg
        elif mode == '2':
            return instructions[relative_base + arg]

    def get_arg_address(arg, mode):
        if mode == '0':
            return arg
        elif mode == '1':
            raise RuntimeError('Invalid mode')
        elif mode == '2':
            return relative_base + arg

    while i < len(instructions):
        instruction = instructions[i]
        instruction_str = '{:0>5}'.format(instruction)
        opcode = instruction_str[3:]

        mode1 = instruction_str[2]
        mode2 = instruction_str[1]
        mode3 = instruction_str[0]

        if opcode == '01':
            arg1 = get_arg_value(instructions[i + 1], mode1)
            arg2 = get_arg_value(instructions[i + 2], mode2)
            arg3 = get_arg_address(instructions[i + 3], mode3)
            instructions[arg3] = arg1 + arg2
            i += 4
        elif opcode == '02':
            arg1 = get_arg_value(instructions[i + 1], mode1)
            arg2 = get_arg_value(instructions[i + 2], mode2)
            arg3 = get_arg_address(instructions[i + 3], mode3)
            instructions[arg3] = arg1 * arg2
            i += 4
        elif opcode == '03':
            arg1 = get_arg_address(instructions[i + 1], mode1)

            while not input_buffer:
                yield

            instructions[arg1] = input_buffer.pop(0)
            i += 2
        elif opcode == '04':
            arg1 = get_arg_value(instructions[i + 1], mode1)
            output_buffer.append(arg1)
            i += 2
        elif opcode == '05':
            arg1 = get_arg_value(instructions[i + 1], mode1)
            arg2 = get_arg_value(instructions[i + 2], mode2)

            if arg1 != 0:
                i = arg2
            else:
                i += 3
        elif opcode == '06':
            arg1 = get_arg_value(instructions[i + 1], mode1)
            arg2 = get_arg_value(instructions[i + 2], mode2)

            if arg1 == 0:
                i = arg2
            else:
                i += 3
        elif opcode == '07':
            arg1 = get_arg_value(instructions[i + 1], mode1)
            arg2 = get_arg_value(instructions[i + 2], mode2)
            arg3 = get_arg_address(instructions[i + 3], mode3)

            instructions[arg3] = 1 if arg1 < arg2 else 0
            i += 4
        elif opcode == '08':
            arg1 = get_arg_value(instructions[i + 1], mode1)
            arg2 = get_arg_value(instructions[i + 2], mode2)
            arg3 = get_arg_address(instructions[i + 3], mode3)

            instructions[arg3] = 1 if arg1 == arg2 else 0
            i += 4
        elif opcode == '09':
            arg1 = get_arg_value(instructions[i + 1], mode1)

            relative_base += arg1
            i += 2
        elif opcode == '99':
            break

if __name__ == '__main__':
    with open(Path(__file__).parent / 'input.txt') as f:
        lines = f.read()

    instructions = [int(x) for x in lines.split(',')]
    instructions.extend([0] * 1024)

    input_buffer = []
    output_buffer = []

    panels = defaultdict(int)
    program = run(instructions, input_buffer, output_buffer)
    position = (0, 0)
    direction = (0, -1)

    input_buffer.append(panels[position])

    left_turns = {
        (0, -1): (-1, 0),
        (-1, 0): (0, 1),
        (0, 1): (1, 0),
        (1, 0): (0, -1),
    }

    for _ in program:

        color, turn = output_buffer
        output_buffer.clear()
        panels[position] = color

        if turn == 0:
            direction = left_turns[direction]
        elif turn == 1:
            direction = left_turns[direction]
            direction = (-direction[0], -direction[1])
        else:
            raise RuntimeError('Wrong turn')

        position = (position[0] + direction[0], position[1] + direction[1])
        input_buffer.append(panels[position])

    print(len(panels))