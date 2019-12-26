from pathlib import Path
from collections import defaultdict

def calculate_pixel(image_data, i, layer_size):
    color = image_data[i]
    layer = 0

    while color == '2':
        layer += 1
        color = image_data[layer * layer_size + i]

    return color

if __name__ == '__main__':
    with open(Path(__file__).parent / 'input.txt') as f:
        image_data = f.read()

    layer_size = 25 * 6
    number_of_layers = len(image_data) // layer_size

    image = [calculate_pixel(image_data, i, layer_size) for i in range(layer_size)]

    for y in range(6):
        print(''.join(image[y * 25: (y + 1) * 25]).replace('0', ' ').replace('1', 'x'))
