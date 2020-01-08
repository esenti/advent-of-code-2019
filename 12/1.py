from pathlib import Path
from re import match
from collections import namedtuple
from itertools import combinations

Vector = namedtuple('Vector', ['x', 'y', 'z'])

class Moon():
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def __repr__(self):
        return 'Moon<{}: {}>'.format(self.position, self.velocity)

    @property
    def energy(self):
        potential_energy = \
            abs(self.position.x) + \
            abs(self.position.y) + \
            abs(self.position.z)

        kinetic_energy = \
            abs(self.velocity.x) + \
            abs(self.velocity.y) + \
            abs(self.velocity.z) 

        return potential_energy * kinetic_energy

    def apply_gravity(self, other):
        self.velocity = Vector(
            self.velocity.x + self.compare(self.position.x, other.position.x),
            self.velocity.y + self.compare(self.position.y, other.position.y),
            self.velocity.z + self.compare(self.position.z, other.position.z)
        )

    def move(self):
        self.position = Vector(
            self.position.x + self.velocity.x,
            self.position.y + self.velocity.y,
            self.position.z + self.velocity.z
        )

    def compare(self, a, b):
        return 1 if a < b else -1 if a > b else 0

def simulate(moons):
    for a, b in combinations(moons, 2):
        a.apply_gravity(b)
        b.apply_gravity(a)

    for moon in moons:
        moon.move()
        
if __name__ == '__main__':
    with open(Path(__file__).parent / 'input.txt') as f:
        lines = f.read().splitlines()

    pattern = r'<x=(-?\d+), y=(-?\d+), z=(-?\d+)>'

    moons = []

    for line in lines:
        m = match(pattern, line)
        x, y, z = [int(i) for i in m.groups()]

        moons.append(Moon(Vector(x, y, z), Vector(0, 0, 0)))

    for _ in range(1000):
        simulate(moons)

    print(sum(moon.energy for moon in moons))
