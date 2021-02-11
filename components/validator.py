from typing import List

from components.competition import Competition


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
                teams_served = [entry[0] for entry in entries]
                t2 = teams_served.count(2)
                t3 = teams_served.count(3)
                t4 = teams_served.count(4)
                result = result and len(pizza_ids) == len(set(pizza_ids)) \
                         and self.teams_of_2 >= t2 \
                         and self.teams_of_3 >= t3 \
                         and self.teams_of_4 >= t4
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
