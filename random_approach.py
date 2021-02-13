import argparse
import multiprocessing
import sys
from multiprocessing import Process

from components.competition import Competition
from components.data_import import read_file
from components.export_result import write_result
from components.pizzeria import Pizzeria
from components.population_generator import generate_pop
from components.score_calculator import ScoreCalculator
from components.validator import Validator

parser = argparse.ArgumentParser(description='Tries using the random generator to solve the problem. '
                                             'It loops ands saves the best solution')

parser.add_argument('-i', '--file', metavar='INPUT_FILE', type=str,
                    help='The file provided with the challenge as an input')
parser.add_argument('-r', '--result', metavar='OUTPUT_FILE', type=str, help='Output file with the best result',
                    default='result')
parser.add_argument('-m', '--max_loops', type=int, help='Number of iterations the program is running', default=100)
parser.add_argument('-s', '--score', type=int, help='The initial score to beat, from previous executions', default=0)


def parallel_generator(id_p: int, comp: Competition, pizz: Pizzeria, result: dict) -> None:
    random_solution = generate_pop(1, comp, pizz)[0]
    result.update({id_p: random_solution})


if __name__ == '__main__':
    args = parser.parse_args()
    if not args.file:
        print("Missing input file.")
        sys.exit(1)

    pizzeria, competition = read_file(args.file)

    validator = Validator(competition, len(pizzeria.pizzas))

    solution = []

    best_score = args.score
    print(f'Initial best score is {best_score} points')
    score_calculator = ScoreCalculator(pizzeria.pizzas)

    num_cores = multiprocessing.cpu_count()

    manager = multiprocessing.Manager()

    for i in range(args.max_loops):
        print(f'iteration {i + 1} of {args.max_loops}')
        result_dict = manager.dict()
        jobs = []
        for x in range(num_cores):
            p = Process(target=parallel_generator, args=(x, competition, pizzeria, result_dict))
            jobs.append(p)
            p.start()

        for proc in jobs:
            proc.join()

        current_best = 0
        best_solution = None
        for result in result_dict.values():
            score = score_calculator.calculate(result)
            if score > current_best:
                current_best = score
                best_solution = result

        if current_best > best_score:
            print(f'Achieved a new best score with {current_best} points')
            best_score = current_best
            write_result(args.result, best_solution)
