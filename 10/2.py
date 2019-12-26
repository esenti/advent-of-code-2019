from pathlib import Path
from math import gcd, atan2, degrees

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

def find_visible_asteroids(ox, oy, space_map):

    blocked_positions = set()
    visible_asteroids = []

    for y, row in enumerate(space_map):
        for x, char in enumerate(row):
            if char == '#' and not (x == ox and y == oy):
                blocked_positions.update(calculate_blocked_positions(ox, oy, x, y, len(row), len(space_map)))

    for y, row in enumerate(space_map):
        for x, char in enumerate(row):
            if char == '#' and not (x == ox and y == oy) and (x, y) not in blocked_positions:
                visible_asteroids.append((x, y))

    return visible_asteroids

def calculate_angle(ox, oy, x, y):
    d = degrees(atan2(y - oy, x - ox)) + 90.0
    d = d if d >= 0.0 else 90.0 - abs(d) + 270.0

    return d

if __name__ == '__main__':
    with open(Path(__file__).parent / 'input.txt') as f:
        lines = f.read().splitlines()

    space_map = []

    for line in lines:
        space_map.append(list(line))

    station = (27, 19)

    visible_asteroids = find_visible_asteroids(station[0], station[1], space_map)
    destroyed_asteroids = []

    while visible_asteroids:
        visible_asteroids.sort(key=lambda i: calculate_angle(station[0], station[1], i[0], i[1]))
        destroyed_asteroids.extend(visible_asteroids)

        for y, row in enumerate(space_map):
            for x, char in enumerate(row):
                if (x, y) in destroyed_asteroids:
                    row[x] = '.'

        visible_asteroids = find_visible_asteroids(station[0], station[1], space_map)

    x, y = destroyed_asteroids[199]
    print(100 * x + y)