from random import sample
from typing import List

from components.competition import Competition
from components.pizzeria import Pizzeria


def generate_pop(num: int, competition: Competition, pizzeria: Pizzeria) -> List[List[List[int]]]:
    result = []
    for _ in range(num):
        orders = []
        teams = {2: competition.teams_of_two, 3: competition.teams_of_three, 4: competition.teams_of_four}
        remaining_people = competition.total_people
        pizza_indexes = list(pizzeria.pizzas.keys())
        while 4 <= len(pizza_indexes) and remaining_people:
            # choose a team
            team = sample([2, 3, 4], counts=[teams[2], teams[3], teams[4]], k=1)[0]
            teams[team] = teams[team] - 1
            order = [team]
            for _ in range(team):
                pizza = sample(pizza_indexes, k=1)
                pizza_indexes.remove(pizza[0])
                order.extend(pizza)
            remaining_people -= team
            orders.append(order)

        # TODO refactor
        if remaining_people >= 2 and len(pizza_indexes) >= 2 :
            if remaining_people == len(pizza_indexes):
                orders.append([remaining_people] + pizza_indexes)
            elif len(pizza_indexes) > remaining_people:
                orders.append([remaining_people] + sample(pizza_indexes, k=remaining_people))
            elif teams[2] + teams[3]:
                if len(pizza_indexes) == 3:
                    if teams[3]:
                        orders.append([3] + pizza_indexes)
                    else:
                        orders.append([2] + pizza_indexes)
                elif teams[2]:
                    orders.append([2] + pizza_indexes)

        result.append(orders)
    return result
