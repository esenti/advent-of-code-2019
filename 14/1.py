from pathlib import Path
from collections import defaultdict, namedtuple

PRETTY_MUCH_INFINITY = 1000000000

Recipe = namedtuple('Recipe', ['amount', 'ingredients'])
Ingredient = namedtuple('Ingredient', ['amount', 'name'])

def make_a_thing(recipes, inventory, thing):
    recipe = recipes[thing]

    for amount, name in recipe.ingredients:
        while inventory[name] < amount:
            make_a_thing(recipes, inventory, name)

        inventory[name] -= amount

    inventory[thing] += recipe.amount

if __name__ == '__main__':
    with open(Path(__file__).parent / 'input.txt') as f:
        lines = f.read().splitlines()

    recipes = {}

    for line in lines:
        ingredients, result = line.split(' => ')
        result_amount, result_name = result.split(' ')

        ii = []
        for i in ingredients.split(', '):
            amount, name = i.split(' ')
            ii.append(Ingredient(int(amount), name))

        recipes[result_name] = Recipe(int(result_amount), ii)

    inventory = defaultdict(int)
    inventory['ORE'] = PRETTY_MUCH_INFINITY

    make_a_thing(recipes, inventory, 'FUEL')

    print(PRETTY_MUCH_INFINITY - inventory['ORE'])