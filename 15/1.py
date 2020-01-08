from pathlib import Path
from collections import defaultdict
from random import randint

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

    game = run(instructions, input_buffer, output_buffer)
    blocks = defaultdict(lambda: ' ')
    position = (0, 0)
    target = (0, 0)
    step = 0
    random_search = True

    for _ in game:
        print(output_buffer)
        if output_buffer:
            v = output_buffer.pop()

            if v == 0:
                blocks[target] = '#'
            elif v == 1:
                blocks[target] = '.'
                position = target
            elif v == 2:
                blocks[target] = 'O'
                position = target
                random_search = False
            else:
                raise RuntimeError('Invalid output!')

        x_max = 0
        y_max = 0
        x_min = 0
        y_min = 0

        for x, y in blocks:
            x_max = max(x_max, x)
            y_max = max(y_max, y)
            x_min = min(x_min, x)
            y_min = min(y_min, y)

        p = blocks[position]
        blocks[(0, 0)] = 'S'
        blocks[position] = 'D'

        print('-' * (x_max  - x_min + 1))
        for y in range(y_min, y_max + 1):
            print(''.join(str(blocks[(x, y)]) for x in range(x_min, x_max + 1)))
        print('-' * (x_max  - x_min + 1))

        blocks[position] = p 

        if random_search:
            if blocks[(position[0], position[1] - 1)] == ' ':
                move = 1
            elif blocks[(position[0], position[1] + 1)] == ' ':
                move = 2
            elif blocks[(position[0] - 1, position[1])] == ' ':
                move = 3
            elif blocks[(position[0] + 1, position[1])] == ' ':
                move = 4
            else:
                move = randint(1, 4)
        else:
            if blocks[(position[0], position[1] - 1)] == 'S' or \
                 blocks[(position[0], position[1] + 1)] == 'S' or \
                 blocks[(position[0] - 1, position[1])] == 'S' or \
                 blocks[(position[0] + 1, position[1])] == 'S':

                print(sum(v == 'x' for v in blocks.values()) + 1)
                break
            elif blocks[(position[0], position[1] - 1)] == '.':
                move = 1
                blocks[position] = 'x'
            elif blocks[(position[0], position[1] + 1)] == '.':
                move = 2
                blocks[position] = 'x'
            elif blocks[(position[0] - 1, position[1])] == '.':
                move = 3
                blocks[position] = 'x'
            elif blocks[(position[0] + 1, position[1])] == '.':
                move = 4
                blocks[position] = 'x'
            elif blocks[(position[0], position[1] - 1)] == 'x':
                move = 1
                blocks[position] = 'b'
            elif blocks[(position[0], position[1] + 1)] == 'x':
                move = 2
                blocks[position] = 'b'
            elif blocks[(position[0] - 1, position[1])] == 'x':
                move = 3
                blocks[position] = 'b'
            elif blocks[(position[0] + 1, position[1])] == 'x':
                move = 4
                blocks[position] = 'b'

        if move == 1:
            target = (position[0], position[1] - 1)
        elif move == 2:
            target = (position[0], position[1] + 1)
        elif move == 3:
            target = (position[0] - 1, position[1])
        elif move == 4:
            target = (position[0] + 1, position[1])
        else:
            print('Invalid input!')
            continue

        print(position, target, step)
        input_buffer.append(move)

        step += 1