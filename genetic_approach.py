import argparse
import copy
import json
import multiprocessing
import sys
from random import shuffle
from typing import List, Tuple

from math import floor, ceil

from components.breeder import Breeder
from components.data_import import read_file
from components.export_result import write_result
from components.population_generator import generate_pop
from components.score_calculator import ScoreCalculator
from components.validator import Validator

parser = argparse.ArgumentParser(description='Tries using a genetic algorithm to solve the problem')

parser.add_argument('-i', '--file', metavar='INPUT_FILE', type=str,
                    help='The file provided with the challenge as an input')
parser.add_argument('-f', '--initial', metavar='POPULATION_FILE', type=str,
                    help='The file with the initial population. Result of previous executions can be used.')
parser.add_argument('-x', '--initial_pop', type=int,
                    help='If not specified the file with the initial population, '
                         'set the number of individuals to generate', default=10)
parser.add_argument('-m', '--max_iterations', type=int, help='Number of iterations the program can be running',
                    default=1000)
parser.add_argument('-n', '--no_improve_stop', type=int,
                    help='If provided, the program will stop after n iterations without an improvement')
parser.add_argument('-s', '--max_pop', type=int,
                    help='Maximum number of individuals, if reachad, the ones with least score are removed',
                    default=100)
parser.add_argument('-e', '--evolution', type=int, help='Number between 0 and 100, probability of mutation', default=10)
parser.add_argument('-r', '--result', metavar='OUTPUT_FILE', type=str, help='Output file with the best result',
                    default='result')
parser.add_argument('-p', '--population', metavar='POPULATION_OUTPUT_FILE', type=str,
                    help='Output file with the population', default='population.json')


def process(process_breeder: Breeder, parent_a: List[List[int]], parent_b: List[List[int]]) \
        -> List[List[List[int]]]:
    new_population = process_breeder.breed(parent_a, parent_b)
    new_population.append(parent_a)
    new_population.append(parent_b)
    return new_population


if __name__ == '__main__':
    args = parser.parse_args()
    if not args.file:
        print("Missing input file.")
        sys.exit(1)

    pizzeria, competition = read_file(args.file)

    if args.initial:
        print('Loading file with initial population')
        with open(args.initial, 'r') as file:
            population = json.load(file).get('population')
    else:
        print('Generating random population')
        population = generate_pop(args.initial_pop, competition, pizzeria)

    num_cores = multiprocessing.cpu_count()

    score_calculator = ScoreCalculator(pizzeria.pizzas)
    print('Calculate initial score')

    population.sort(key=score_calculator.calculate, reverse=True)

    best_score = score_calculator.calculate(population[0])

    print(f'Initial best score is {best_score} poitns')
    iterations_without_improvement = 0

    validator = Validator(competition, len(pizzeria.pizzas))
    breeder = Breeder(list(pizzeria.pizzas.keys()), validator, competition, args.evolution)

    pool = multiprocessing.Pool(processes=num_cores)

    print('-' * 30)
    for i in range(args.max_iterations):
        print(f'Iteration {i} of {args.max_iterations}')
        # make pairs
        shuffle(population)
        new_pop = []
        num_pairs = floor(len(population) / 2)
        pairs = []

        for i in range(num_pairs):
            parent_a = population[i * 2]
            parent_b = population[1 + i * 2]
            pairs.append((breeder, parent_a, parent_b))

        results = pool.starmap(process, pairs)
        new_pop = [pop for result in results for pop in result]
        if len(population) % 2:
            new_pop.extend(population[num_pairs * 2:])
        population = copy.deepcopy(new_pop)
        # breed
        # calcule score and order according
        population.sort(key=score_calculator.calculate, reverse=True)
        new_best_score = score_calculator.calculate(population[0])
        print(f'Current best score is {new_best_score} points')
        # print(population[0])
        # if score not increased in n iterations, break
        if new_best_score > best_score:
            iterations_without_improvement = 0
            best_score = new_best_score
        else:
            iterations_without_improvement += 1
            print(f'{iterations_without_improvement} iterations without an improvement')
            if args.no_improve_stop and iterations_without_improvement == args.no_improve_stop:
                print(f'Finishing early cause no improvement after {args.no_improve_stop} iterations')
                break
        # remove individuals with poor score
        if len(population) > args.max_pop:
            population = population[:args.max_pop]
    score = score_calculator.calculate(population[0])
    print(f'Best solution has a score of {score} points')

    with open(args.population, 'w') as outfile:
        json.dump({"population": population}, outfile)

    write_result(args.result, population[0])
