from pathlib import Path
from re import match
from collections import namedtuple
from itertools import combinations

class Moon():
    def __init__(self, position, velocity):
        self.state = position + velocity

    def __repr__(self):
        return 'Moon<{}>'.format(self.state)

    @property
    def energy(self):
        potential_energy = \
            abs(self.state[0]) + \
            abs(self.state[1]) + \
            abs(self.state[2])

        kinetic_energy = \
            abs(self.state[3]) + \
            abs(self.state[4]) + \
            abs(self.state[5]) 

        return potential_energy * kinetic_energy

    def __hash__(self):
        return hash(tuple(self.state))

    def apply_gravity(self, other):
        x = self.compare(self.state[0], other.state[0])
        y = self.compare(self.state[1], other.state[1])
        z = self.compare(self.state[2], other.state[2])
        self.state[3] += x
        self.state[4] += y
        self.state[5] += z
        other.state[3] -= x
        other.state[4] -= y
        other.state[5] -= z

    def move(self):
        self.state[0] += self.state[3]
        self.state[1] += self.state[4]
        self.state[2] += self.state[5]

    def compare(self, a, b):
        return 1 if a < b else -1 if a > b else 0

def simulate(moons):
    for a, b in combinations(moons, 2):
        a.apply_gravity(b)

    for moon in moons:
        moon.move()
        
if __name__ == '__main__':
    with open(Path(__file__).parent / 'input.txt') as f:
        lines = f.read().splitlines()

    pattern = r'<x=(-?\d+), y=(-?\d+), z=(-?\d+)>'

    moons = []
    initial_moons = []

    for line in lines:
        m = match(pattern, line)
        x, y, z = [int(i) for i in m.groups()]

        moons.append(Moon([x, y, z], [0, 0, 0]))
        initial_moons.append(Moon([x, y, z], [0, 0, 0]))

    finished = False
    count = 0
    states = set()

    import time

    start = time.clock()

    while True:# and count != 1000000:
        simulate(moons)

        h = tuple(hash(moon) for moon in moons)

        if h not in states:
            states.add(h)
        else:
            break

        count += 1

        if not count % 50000:
            print(count)

    end = time.clock()

    print('-' * 10)
    print(count)
    print(end - start)

    print(moons)
