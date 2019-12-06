from pathlib import Path

def calculate_fuel(mass):

    fuel = max(int(int(mass) / 3) - 2, 0)

    return fuel + (calculate_fuel(fuel) if fuel > 0 else 0)

if __name__ == '__main__':
    with open(Path(__file__).parent / 'input.txt') as f:
        lines = f.readlines()

    result = sum([calculate_fuel(mass) for mass in lines])

    print(result)