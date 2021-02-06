from copy import copy
from random import sample
from typing import List

from components.validator import Validator


class Breeder:
    def __init__(self, pizzas: List[int], validator: Validator, mutation_factor:int) -> None:
        self.pizzas_indexes = pizzas
        self.validator = validator
        self.mutation_factor = mutation_factor

    def breed(self, parent_a:List[List[int]], parent_b:List[List[int]]) -> List[List[List[int]]]:
        min_length = min(len(parent_a), len(parent_b))
        cut_point = sample(range(min_length), k=1)[0]

        a_1 = parent_a[:cut_point]
        a_2 = parent_a[cut_point:]

        b_1 = parent_b[:cut_point]
        b_2 = parent_b[cut_point:]

        child_a = a_1 + b_2
        child_b = b_1 + a_2
        child_c = b_2 + a_1
        child_d = a_2 + b_1

        self.verify_and_correct(child_a)
        self.verify_and_correct(child_b)
        self.verify_and_correct(child_c)
        self.verify_and_correct(child_d)

        return [child_a, child_b, child_c, child_d]

    # TODO refactor
    def verify_and_correct(self, child):
        if not self.validator.validate(child):
            used_pizzas = [pizza for order in child for pizza in order[1:]]
            available_pizzas = [pizza for pizza in self.pizzas_indexes if pizza not in used_pizzas]
            duplicates = copy(used_pizzas)
            for x in list(set(used_pizzas)):
                duplicates.remove(x)
            if available_pizzas:
                while True:
                    for order in child:
                        for i in range(len(order)-1):
                            if order[i+1] in duplicates and len(available_pizzas):
                                duplicates.remove(order[i+1])
                                pizza = available_pizzas.pop()
                                order[i+1] = pizza
                    if not duplicates or not available_pizzas:
                        break
            else:
                order_to_remove = None
                for order in child:
                    for i in range(len(order) - 1):
                        if order[i + 1] in duplicates:
                            order_to_remove = order
                            break
                    if order_to_remove:
                        break
                child.remove(order_to_remove)
                self.validator.validate(child)





