from pathlib import Path

if __name__ == '__main__':
    with open(Path(__file__).parent / 'input.txt') as f:
        lines = f.readlines()

    result = sum([int(int(mass) / 3) - 2 for mass in lines])

    print(result)