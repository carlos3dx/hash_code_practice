from typing import Dict, List


class ScoreCalculator:
    def __init__(self, pizzas: Dict[int, List[int]]):
        self.pizzas = pizzas

    def calculate(self, entries: List[List[int]]) -> int:
        if len(entries) == 0:
            result = 0
        else:
            result = sum(map(self.calculate_entry, entries))
        return result

    def calculate_entry(self, entry: List[int]) -> int:
        ingredients = []
        for pizza in entry[1:]:
            ingredients.extend(self.pizzas.get(pizza))
        return len(set(ingredients))**2
