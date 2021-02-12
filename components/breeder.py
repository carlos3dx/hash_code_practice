from copy import deepcopy
from random import sample, choices, randint
from typing import List

from components.competition import Competition
from components.validator import Validator


class Breeder:
    def __init__(self, pizzas: List[int], validator: Validator, competition: Competition, mutation_factor: int) -> None:
        self.pizzas_indexes = pizzas
        self.validator = validator
        self.competition = competition
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

    def verify_and_correct(self, child: List[List[int]]) -> List[List[int]]:
        result = deepcopy(child)
        while not self.validator.validate(result):
            used_pizzas = [pizza for order in result for pizza in order[1:]]
            available_pizzas = [pizza for pizza in self.pizzas_indexes if pizza not in used_pizzas]
            duplicates = used_pizzas[:]
            for x in list(set(used_pizzas)):
                duplicates.remove(x)
            if len(result) > self.competition.total_teams:
                result = self.remove_extra_order(result, choices([2, 3, 4], k=1)[0])
            else:
                if duplicates:
                    result = self.correct_duplicates(available_pizzas, duplicates, result)
                else:
                    result = self.correct_exceeded_teams(available_pizzas, result)
        return result

    def correct_duplicates(self, available_pizzas: List[int], duplicates: List[int],
                           child: List[List[int]]) -> List[List[int]]:
        if available_pizzas:
            result = self.correct_duplicates_with_available_pizzas(available_pizzas, duplicates, child)
        else:
            result = self.correct_duplicates_without_available_pizzas(duplicates, child)
        return result

    def correct_duplicates_with_available_pizzas(self, available_pizzas: List[int], duplicates: List[int],
                                                 child: List[List[int]]) -> List[List[int]]:
        new_child = []
        for order in child:
            if any(map(lambda x: x in duplicates, order[1:])):
                new_order = [order[0]]
                for pizza in order[1:]:
                    if pizza in duplicates and available_pizzas:
                        duplicates.remove(pizza)
                        new_order.append(available_pizzas.pop())
                    else:
                        new_order.append(pizza)
                new_child.append(new_order)
            else:
                new_child.append(order)
        return new_child

    def correct_duplicates_without_available_pizzas(self, duplicates: List[int], child: List[List[int]]) -> List[
        List[int]]:
        new_child = []
        for order in child:
            order_to_remove = None
            for i in range(len(order) - 1):
                if order[i + 1] in duplicates:
                    duplicates.remove(order[i + 1])
                    order_to_remove = order
            if order_to_remove is None:
                new_child.append(order)
        return new_child

    def correct_exceeded_teams(self, available_pizzas: List[int], child: List[List[int]]) -> List[List[int]]:
        used_teams = [order[0] for order in child]
        availability = {2: self.competition.teams_of_two - used_teams.count(2),
                        3: self.competition.teams_of_three - used_teams.count(3),
                        4: self.competition.teams_of_four - used_teams.count(4)}
        team_to_modify = None
        for key, value in availability.items():
            if value < 0:
                team_to_modify = key
                break

        teams_available = []
        for key, value in availability.items():
            if value > 0:
                teams_available.append(key)

        if team_to_modify and teams_available:
            max_team = max(teams_available)
            min_team = min(teams_available)
            if team_to_modify < max_team <= len(available_pizzas):
                result = self.upsize_team(child, team_to_modify, max_team, available_pizzas)
            elif team_to_modify < min_team:
                result = self.upsize_team(child, team_to_modify, min_team, available_pizzas)
            else:
                result = self.downsize_team(child, team_to_modify, max_team if max_team < team_to_modify else min_team)
        else:
            result = self.remove_extra_order(child, team_to_modify)

        return result

    @staticmethod
    def downsize_team(child: List[List[int]], target_team: int, new_team: int) -> List[List[int]]:
        result = []
        downsized = False
        for order in child:
            if not downsized and order[0] == target_team:
                downsized = True
                result.append([new_team] + order[1:new_team - target_team])
            else:
                result.append(order)
        return result

    @staticmethod
    def upsize_team(child: List[List[int]], target_team: int, new_team: int, available_pizzas) -> List[List[int]]:
        result = []
        upsized = False
        for order in child:
            if not upsized and order[0] == target_team:
                upsized = True
                result.append([new_team] + order[1:] + available_pizzas[:new_team - target_team])
            else:
                result.append(order)
        return result

    @staticmethod
    def remove_extra_order(child: List[List[int]], target_team: int) -> List[List[int]]:
        result = []
        removed = False
        for order in child:
            if not removed and order[0] == target_team:
                removed = True
            else:
                result.append(order)
        return result

    def mutate(self, child: List[List[int]]) -> List[List[int]]:
        mutate = choices([True, False], cum_weights=[self.mutation_factor, 100], k=1)[0]
        new_child = deepcopy(child)
        if mutate:
            used_pizzas = [pizza for order in child for pizza in order[1:]]
            available_pizzas = [pizza for pizza in self.pizzas_indexes if pizza not in used_pizzas]
            if available_pizzas:
                order_index = randint(0, len(child) - 1)
                order_pizza_index = randint(1, len(child[order_index]) - 1)
                new_pizza = sample(available_pizzas, k=1)[0]
                new_child[order_index][order_pizza_index] = new_pizza
            else:
                orders_indexes = sample(range(len(child)), k=2)
                order_a_pizza_index = randint(1, len(child[orders_indexes[0]]) - 1)
                order_b_pizza_index = randint(1, len(child[orders_indexes[1]]) - 1)
                new_child[orders_indexes[0]][order_a_pizza_index], new_child[orders_indexes[1]][order_b_pizza_index] = \
                    new_child[orders_indexes[1]][order_b_pizza_index], new_child[orders_indexes[0]][order_a_pizza_index]
        return new_child
