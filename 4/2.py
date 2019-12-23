from pathlib import Path
from itertools import tee

def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

def validate(number):
    has_pair = False
    same_count = 0

    for a, b in pairwise(number):
        if a > b:
            return False
        if a == b:
            same_count += 1
        else:
            if same_count == 1:
                has_pair = True

            same_count = 0

    return has_pair or same_count == 1

if __name__ == '__main__':
    with open(Path(__file__).parent / 'input.txt') as f:
        content = f.read()

    start, end = content.split('-')
    start = int(start)
    end = int(end)

    count = sum(validate(str(x)) for x in range(start, end + 1))
    print(count)