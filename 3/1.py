from pathlib import Path
from math import inf

def calculate_line(moves):
    position = (0, 0)
    visited_positions = set() 

    for move in moves:
        position = make_move(move, position, visited_positions)

    return visited_positions

def make_move(move, position, visited_positions):

    direction = move[0]
    amount = int(move[1:])
    new_position = position

    for _ in range(amount):
        new_position = calculate_move(direction, new_position)
        visited_positions.add(new_position)

    return new_position

def calculate_move(direction, position):
    if direction == 'U':
        new_position = (position[0], position[1] + 1)
    elif direction == 'D':
        new_position = (position[0], position[1] - 1)
    elif direction == 'L':
        new_position = (position[0] - 1, position[1])
    elif direction == 'R':
        new_position = (position[0] + 1, position[1])

    return new_position

if __name__ == '__main__':
    with open(Path(__file__).parent / 'input.txt') as f:
        lines = f.readlines()
        
    visited_positions_first = calculate_line(lines[0].split(','))
    visited_positions_second = calculate_line(lines[1].split(','))

    intersections = visited_positions_first & visited_positions_second

    minimum_distance = inf

    for x, y in intersections:
        distance = abs(x) + abs(y)
        if distance < minimum_distance:
            minimum_distance = distance

    print(minimum_distance)