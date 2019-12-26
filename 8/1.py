from pathlib import Path
from collections import defaultdict

if __name__ == '__main__':
    with open(Path(__file__).parent / 'input.txt') as f:
        image_data = f.read()

    layer_size = 25 * 6
    layers = defaultdict(lambda: defaultdict(int)) 

    for i, digit in enumerate(image_data):
        layer_number = i // layer_size
        layers[layer_number][digit] += 1

    min_zeros = min(layers.values(), key=lambda x: x['0'])
    print(min_zeros['1'] * min_zeros['2'])