from components.competition import Competition
from components.pizzeria import Pizzeria
from components.population_generator import generate_pop
from components.validator import Validator


class TestPopulationGenerator:
    def test_generate_possible_valid_solutions_minimizing_waste_more_people_than_pizzas(self):
        pizzas = {0: [0, 1, 2],
                  1: [3, 4, 5],
                  2: [6, 3, 1],
                  3: [4, 3, 5],
                  4: [6, 5]}
        pizzeria = Pizzeria(pizzas, 7)
        competition = Competition(1, 2, 1)
        num_pizzas = len(pizzeria.pizzas)
        validator = Validator(competition, num_pizzas)

        num_results = 10

        results = generate_pop(num_results, competition, pizzeria)

        assert len(results) == num_results

        for result in results:
            assert validator.validate(result)
            remaining_pizzas = num_pizzas - sum([len(x[1:]) for x in result])
            remaining_people = competition.total_people - sum([x[0] for x in result])
            assert remaining_people > remaining_pizzas

    def test_generate_possible_valid_solutions_minimizing_waste_more_pizzas_than_people(self):
        pizzas = {0: [0, 1, 2],
                  1: [3, 4, 5],
                  2: [3, 4, 5],
                  3: [3, 4, 5],
                  4: [3, 4, 5],
                  5: [3, 4, 5],
                  6: [6, 3, 1],
                  7: [6, 3, 1],
                  8: [6, 3, 1],
                  9: [6, 3, 1],
                  10: [4, 3, 5],
                  11: [4, 3, 5],
                  12: [4, 3, 5],
                  13: [4, 3, 5],
                  14: [6, 5]}
        pizzeria = Pizzeria(pizzas, 7)
        competition = Competition(2, 2, 0)
        num_pizzas = len(pizzeria.pizzas)
        validator = Validator(competition, num_pizzas)

        num_results = 10

        results = generate_pop(num_results, competition, pizzeria)

        assert len(results) == num_results

        for result in results:
            assert validator.validate(result)
            remaining_people = competition.total_people - sum([x[0] for x in result])
            assert not remaining_people

    def test_generate_possible_valid_solutions_minimizing_waste_way_more_people_than_pizzas(self):
        pizzas = {0: [0, 1, 2],
                  1: [3, 4, 5],
                  2: [3, 4, 5],
                  3: [3, 4, 5],
                  4: [3, 4, 5],
                  5: [3, 4, 5],
                  6: [6, 3, 1],
                  7: [6, 3, 1],
                  8: [6, 3, 1],
                  9: [6, 3, 1],
                  10: [4, 3, 5],
                  11: [4, 3, 5],
                  12: [4, 3, 5],
                  13: [4, 3, 5],
                  14: [6, 5]}
        pizzeria = Pizzeria(pizzas, 7)
        competition = Competition(40, 20, 10)
        num_pizzas = len(pizzeria.pizzas)
        validator = Validator(competition, num_pizzas)

        num_results = 10

        results = generate_pop(num_results, competition, pizzeria)

        assert len(results) == num_results

        for result in results:
            assert validator.validate(result)
            remaining_pizzas = num_pizzas - sum([len(x[1:]) for x in result])
            remaining_people = competition.total_people - sum([x[0] for x in result])
            assert remaining_people > remaining_pizzas
