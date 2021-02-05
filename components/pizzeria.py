class Pizzeria:
    def __init__(self, pizzas: dict, num_ingredients: int) -> None:
        self.pizzas = pizzas
        self.num_ingredients = num_ingredients

    def __eq__(self, other):
        return isinstance(other, Pizzeria) and \
               self.pizzas == other.pizzas and \
               self.num_ingredients == other.num_ingredients
