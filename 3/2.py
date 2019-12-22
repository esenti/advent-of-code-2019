from pathlib import Path
from math import inf

def calculate_line(moves):
    position = (0, 0)
    visited_positions = {} 
    cost = 0

    for move in moves:
        position, cost = make_move(move, position, visited_positions, cost)

    return visited_positions

def make_move(move, position, visited_positions, cost):

    direction = move[0]
    amount = int(move[1:])
    new_position = position

    for _ in range(amount):
        new_position = calculate_move(direction, new_position)
        cost += 1

        if new_position not in visited_positions.keys():
            visited_positions[new_position] = cost

    return new_position, cost

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

    intersections = visited_positions_first.keys() & visited_positions_second.keys()

    minimum_distance = inf

    for intersection in intersections:
        distance = visited_positions_first[intersection] + visited_positions_second[intersection]
        if distance < minimum_distance:
            minimum_distance = distance

    print(minimum_distance)