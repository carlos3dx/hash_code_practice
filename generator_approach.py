import argparse
import copy
import multiprocessing
import sys
from multiprocessing import Lock
from random import sample
from typing import List

from components.data_import import read_file
from components.export_result import write_result
from components.pizzeria import Pizzeria
from components.score_calculator import ScoreCalculator
from components.validator import Validator

parser = argparse.ArgumentParser(description='Tries using a customised generator to solve the problem')

parser.add_argument('-i', '--file', metavar='INPUT_FILE', type=str,
                    help='The file provided with the challenge as an input')
parser.add_argument('-f', '--initial', metavar='POPULATION_FILE', type=str,
                    help='The file with the initial population. Result of previous executions can be used.')
parser.add_argument('-r', '--result', metavar='OUTPUT_FILE', type=str, help='Output file with the best result',
                    default='result')
parser.add_argument('-t', '--team', type=int, help='The number of the team which will try to complete orders first',
                    default=4)
parser.add_argument('-u', '--second_team', type=int, help='The number of the team which will try to complete orders '
                                                          'in second place. If not specified it would be chosen '
                                                          'randomly')


def create_order(team_type: int, available_pizzas: dict, pizz: Pizzeria, lock: Lock) -> [List[int]]:
    order = [team_type]
    for x in range(team_type):
        print()
        if x:
            pass
        # Else
            # get used ingredients
            # find using the reverse index the pizza that shares the least amount ingredients with those in use and
            #    has the most different ingredients
            # get lock and proceed like the other case
        else:
            done = False
            while not done:
                p_id = sample(available_pizzas.keys(), k=1)[0]
                with lock:
                    if p_id in available_pizzas.keys():
                        done = True
                        order.append(p_id)
    return order


if __name__ == '__main__':
    args = parser.parse_args()
    if not args.file:
        print("Missing input file.")
        sys.exit(1)

    pizzeria, competition = read_file(args.file)

    validator = Validator(competition, len(pizzeria.pizzas))
    score_calculator = ScoreCalculator(pizzeria.pizzas)

    first_team = args.team
    if args.second_team:
        teams = [x for x in range(2, 5) if x != first_team]
        second_team = sample(teams, k=1)[0]
    else:
        second_team = args.second_team

    teams_list = [first_team, second_team]
    teams_list.extend([x for x in range(2, 5) if x not in teams_list])
    pizza_lock = Lock()
    orders_to_fill = []
    pizzas_available = len(pizzeria.pizzas)
    manager = multiprocessing.Manager()
    pizzas = manager.dict()
    pizzas.update(pizzeria.pizzas)
    for team in teams_list:
        while pizzas_available >= team:
            orders_to_fill.append((team, pizzas, pizzeria, pizza_lock))
            pizzas_available -= team

    num_cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=num_cores)
    solution = pool.starmap(create_order, orders_to_fill)

    valid = validator.validate(solution)
    if valid:
        score = score_calculator.calculate(solution)
        print(f'Obtained a solution with an score of {score} points')
    else:
        print('The solution is not valid, but saved to check what went wrong')
    write_result(args.result, solution)

