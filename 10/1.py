from pathlib import Path
from math import gcd

def calculate_blocked_positions(ox, oy, bx, by, width, height):
    dx = bx - ox
    dy = by - oy

    d = gcd(dx, dy)
    dx = dx // d
    dy = dy // d

    positions = []

    x = bx + dx
    y = by + dy

    while x >= 0 and y >= 0 and x < width and y < height:
        positions.append((x, y))
        x += dx
        y += dy

    return positions

def count_visible_asteroids(ox, oy, space_map):

    blocked_positions = set()
    count = 0

    for y, row in enumerate(space_map):
        for x, char in enumerate(row):
            if char == '#' and not (x == ox and y == oy):
                blocked_positions.update(calculate_blocked_positions(ox, oy, x, y, len(row), len(space_map)))

    for y, row in enumerate(space_map):
        for x, char in enumerate(row):
            if char == '#' and not (x == ox and y == oy) and (x, y) not in blocked_positions:
                count += 1

    return count

if __name__ == '__main__':
    with open(Path(__file__).parent / 'input.txt') as f:
        lines = f.read().splitlines()

    space_map = []

    for line in lines:
        space_map.append(list(line))

    visible_asteroids = []

    for y, row in enumerate(space_map):
        for x, char in enumerate(row):
            if char == '#':
                visible_asteroids.append((x, y, count_visible_asteroids(x, y, space_map)))

    print(max(visible_asteroids, key=lambda x: x[2]))