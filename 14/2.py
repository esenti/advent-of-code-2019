from pathlib import Path
from collections import defaultdict, namedtuple

PRETTY_MUCH_INFINITY = 1000000000

Recipe = namedtuple('Recipe', ['amount', 'ingredients'])
Ingredient = namedtuple('Ingredient', ['amount', 'name'])

def make_a_thing(recipes, inventory, thing):

    if thing == 'ORE':
        return False

    recipe = recipes[thing]

    for amount, name in recipe.ingredients:
        while inventory[name] < amount:
            if not make_a_thing(recipes, inventory, name):
                return False

        inventory[name] -= amount

    inventory[thing] += recipe.amount
    return True

if __name__ == '__main__':
    with open(Path(__file__).parent / 'input.txt') as f:
        lines = f.read().splitlines()

    recipes = {}
    bulk_recipes = {}

    for line in lines:
        ingredients, result = line.split(' => ')
        result_amount, result_name = result.split(' ')

        ii = []
        bii = []
        for i in ingredients.split(', '):
            amount, name = i.split(' ')
            ii.append(Ingredient(int(amount), name))
            bii.append(Ingredient(int(amount) * 10000, name))

        recipes[result_name] = Recipe(int(result_amount), ii)
        bulk_recipes[result_name] = Recipe(int(result_amount) * 10000, bii)

    inventory = defaultdict(int)
    inventory['ORE'] = PRETTY_MUCH_INFINITY
    make_a_thing(recipes, inventory, 'FUEL')

    fuel_cost = PRETTY_MUCH_INFINITY - inventory['ORE']

    inventory = defaultdict(int)
    inventory['ORE'] = 1000000000000

    while inventory['ORE'] > 10000000000:
        make_a_thing(bulk_recipes, inventory, 'FUEL')
        print(inventory['FUEL'])

    while make_a_thing(recipes, inventory, 'FUEL'):
        print(inventory['FUEL'])

    print(fuel_cost)
    print(inventory)
    print(inventory['FUEL'])