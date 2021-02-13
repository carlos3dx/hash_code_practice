import argparse
import sys
from random import sample

from components.data_import import read_file
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

if __name__ == '__main__':
    args = parser.parse_args()
    if not args.file:
        print("Missing input file.")
        sys.exit(1)

    pizzeria, competition = read_file(args.file)

    validator = Validator(competition, len(pizzeria.pizzas))

    solution = []

    first_team = args.team
    if args.second_team:
        teams = [x for x in range(2, 5) if x != first_team]
        second_team = sample(teams, k=1)[0]
    else:
        second_team = args.second_team

    teams_list = [first_team, second_team]
    teams_list.extend([x for x in range(2, 5) if x not in teams_list])
