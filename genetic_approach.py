import argparse
import json
import sys

from components.data_import import read_file

parser = argparse.ArgumentParser(description='Tries using a genetic algorithm to solve the problem')

parser.add_argument('-f', '--file', metavar='INPUT_FILE', type=str,
                    help='The file provided with the challenge as an input')
parser.add_argument('-i', '--initial', metavar='POPULATION_FILE', type=str,
                    help='The file with the initial population. Result of previous executions can be used.')
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

if __name__ == '__main__':
    args = parser.parse_args()
    if not args.file:
        print("Missing input file.")
        sys.exit(1)

    pizzeria, competition = read_file(args.file)

    if args.initial:
        with open(args.initial, 'r') as file:
            population = json.load(file).get('population')
    else:

