from copy import deepcopy
from random import sample, choices, randint
from typing import List

from components.validator import Validator


class Breeder:
    def __init__(self, pizzas: List[int], validator: Validator, mutation_factor: int) -> None:
        self.pizzas_indexes = pizzas
        self.validator = validator
        self.mutation_factor = mutation_factor

    def breed(self, parent_a: List[List[int]], parent_b: List[List[int]]) -> List[List[List[int]]]:
        min_length = min(len(parent_a), len(parent_b))
        cut_point = sample(range(1, max(min_length - 1, 2)), k=1)[0]

        a_1 = parent_a[:cut_point]
        a_2 = parent_a[cut_point:]

        b_1 = parent_b[:cut_point]
        b_2 = parent_b[cut_point:]

        child_a = deepcopy(a_1 + b_2)
        child_b = deepcopy(b_1 + a_2)
        child_c = deepcopy(b_2 + a_1)
        child_d = deepcopy(a_2 + b_1)

        result = [self.verify_and_correct(child_a),
                  self.verify_and_correct(child_b),
                  self.verify_and_correct(child_c),
                  self.verify_and_correct(child_d)]

        return [self.mutate(x) for x in result]

    # TODO refactor
    def verify_and_correct(self, child):
        new_child = []
        if not self.validator.validate(child):
            used_pizzas = [pizza for order in child for pizza in order[1:]]
            available_pizzas = [pizza for pizza in self.pizzas_indexes if pizza not in used_pizzas]
            duplicates = deepcopy(used_pizzas)
            for x in list(set(used_pizzas)):
                duplicates.remove(x)
            if available_pizzas:
                while True:
                    for order in child:
                        new_order = [order[0]]
                        for i in range(len(order) - 1):
                            if order[i + 1] in duplicates:
                                if len(available_pizzas):
                                    duplicates.remove(order[i + 1])
                                    new_order.append(available_pizzas.pop())
                                else:
                                    if len(new_order) >= 2:
                                        for x in new_order[1:]:
                                            available_pizzas.append(x)
                                        for x in order[1:]:
                                            if x in duplicates:
                                                duplicates.remove(x)
                                    new_order = None
                                    break
                            else:
                                new_order.append(order[i + 1])
                        if new_order:
                            new_child.append(new_order)
                    if not duplicates or not available_pizzas:
                        break
            else:
                for order in child:
                    order_to_remove = None
                    for i in range(len(order) - 1):
                        if order[i + 1] in duplicates:
                            duplicates.remove(order[i + 1])
                            order_to_remove = order
                    if order_to_remove is None:
                        new_child.append(order)
                new_child = self.verify_and_correct(new_child)
        else:
            new_child = child
        return new_child

    def mutate(self, child: List[List[int]]) -> List[List[int]]:
        mutate = choices([True, False], cum_weights=[self.mutation_factor, 100], k=1)[0]
        new_child = deepcopy(child)
        if mutate:
            used_pizzas = [pizza for order in child for pizza in order[1:]]
            available_pizzas = [pizza for pizza in self.pizzas_indexes if pizza not in used_pizzas]
            if available_pizzas:
                order_index = randint(0, len(child)-1)
                order_pizza_index = randint(1, len(child[order_index])-1)
                new_pizza = sample(available_pizzas, k=1)[0]
                new_child[order_index][order_pizza_index] = new_pizza
            else:
                orders_indexes = sample(range(len(child)), k=2)
                order_a_pizza_index = randint(1, len(child[orders_indexes[0]]) - 1)
                order_b_pizza_index = randint(1, len(child[orders_indexes[1]]) - 1)
                new_child[orders_indexes[0]][order_a_pizza_index], new_child[orders_indexes[1]][order_b_pizza_index] = \
                    new_child[orders_indexes[1]][order_b_pizza_index], new_child[orders_indexes[0]][order_a_pizza_index]
        return new_child

