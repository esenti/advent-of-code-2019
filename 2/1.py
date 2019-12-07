from pathlib import Path

if __name__ == '__main__':
    with open(Path(__file__).parent / 'input.txt') as f:
        lines = f.read()

    instructions = [int(x) for x in lines.split(',')]

    instructions[1] = 12
    instructions[2] = 2

    i = 0
    while i < len(instructions):
        opcode = instructions[i]
        arg1_address = instructions[i + 1]
        arg2_address = instructions[i + 2]
        result_address = instructions[i + 3]

        if opcode == 1:
            instructions[result_address] = instructions[arg1_address] + instructions[arg2_address]
        elif opcode == 2:
            instructions[result_address] = instructions[arg1_address] * instructions[arg2_address]
        elif opcode == 99:
            break

        i += 4

    print(','.join(str(x) for x in instructions))