from typing import List

from competition import Competition


class Validator:
    def __init__(self, competition: Competition, num_pizzas: int):
        self.teams_of_2 = competition.teams_of_two
        self.teams_of_3 = competition.teams_of_three
        self.teams_of_4 = competition.teams_of_four
        self.num_teams = competition.total_teams
        self.num_pizzas = num_pizzas

    def validate(self, entries: List[List[int]]) -> bool:
        if len(entries) == 0:
            result = True
        else:
            result = len(entries) <= self.num_teams and \
                     all(self.validate_entry(entry) for entry in entries)
            if result:
                pizza_ids = [pizza_id for entry in entries for pizza_id in entry[1:]]
                result = result and len(pizza_ids) == len(set(pizza_ids))
        return result

    def validate_entry(self, entry: List[int]) -> bool:
        if len(entry) == 0:
            result = False
        else:
            pizzas = entry[1:]
            valid_numbers = len(set(pizzas)) == entry[0]  # number of people not equal to pizzas
            valid_ids = all(i < self.num_pizzas for i in pizzas)
            result = valid_numbers and valid_ids
        return result
