from pathlib import Path

def count_orbits(planets, name):
    if name == 'COM':
        return 0
    else:
        return 1 + count_orbits(planets, planets[name])

if __name__ == '__main__':
    with open(Path(__file__).parent / 'input.txt') as f:
        lines = f.read().splitlines()

    planets = {}

    for line in lines:
        orbited, orbiting = line.split(')')
        planets[orbiting] = orbited

    print(sum(count_orbits(planets, planet) for planet in planets))