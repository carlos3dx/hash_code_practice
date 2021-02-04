from typing import Tuple

from competition import Competition
from pizzeria import Pizzeria


def read_file(file_path: str) -> Tuple[Pizzeria, Competition]:
    pizzas = {}
    ingredients = {}
    pizza_pointer = 0
    ingredient_pointer = 0
    with open(file_path, 'r') as file:
        header = file.readline().split(' ')
        num_pizzas = int(header[0])
        t2 = int(header[1])
        t3 = int(header[2])
        t4 = int(header[3])
        for _ in range(num_pizzas):
            line = file.readline().replace('\n', '').split(' ')
            pizza_ingredients_text = line[1:]
            pizza_ingredients = []
            for ingredient in pizza_ingredients_text:
                if ingredient not in ingredients.keys():
                    ingredients[ingredient] = ingredient_pointer
                    index = ingredient_pointer
                    ingredient_pointer += 1
                else:
                    index = ingredients.get(ingredient)
                pizza_ingredients.append(index)
            pizzas[pizza_pointer] = pizza_ingredients
            pizza_pointer += 1

    return Pizzeria(pizzas, len(ingredients)), Competition(t2, t3, t4)
