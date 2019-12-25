from pathlib import Path

def count_orbits(planets, name, center):
    if name == center:
        return 0
    else:
        return 1 + count_orbits(planets, planets[name], center)

def find_path(planets, name):
    if name == 'COM':
        return ['COM']
    else:
        path = find_path(planets, planets[name])
        return path + [name]

if __name__ == '__main__':
    with open(Path(__file__).parent / 'input.txt') as f:
        lines = f.read().splitlines()

    planets = {}

    for line in lines:
        orbited, orbiting = line.split(')')
        planets[orbiting] = orbited

    you = find_path(planets, planets['YOU'])
    santa = find_path(planets, planets['SAN'])

    last_common = None

    for a, b in zip(you, santa):
        if a == b:
            last_common = a
        else:
            break

    you_count = count_orbits(planets, planets['YOU'], last_common)
    santa_count = count_orbits(planets, planets['SAN'], last_common)

    print(you_count + santa_count)