class Pizzeria:
    def __init__(self, pizzas: dict, num_ingredients: int) -> None:
        self.pizzas = pizzas
        self.num_ingredients = num_ingredients
        self._ingredients_reverse_index()

    def __eq__(self, other):
        return isinstance(other, Pizzeria) and \
               self.pizzas == other.pizzas and \
               self.num_ingredients == other.num_ingredients

    def _ingredients_reverse_index(self):
        self.ingredients_reverse_index = {}
        for pizza_key, pizza_value in self.pizzas.items():
            for ingredient in pizza_value:
                ingredient_list = self.ingredients_reverse_index.get(ingredient, [])
                ingredient_list.append(pizza_key)
                self.ingredients_reverse_index[ingredient] = ingredient_list
