import os

from components.competition import Competition
from components.data_import import read_file
from components.pizzeria import Pizzeria

test_files_path = os.path.abspath(os.path.dirname(__file__))


class TestDataImport:
    def test_import_example_a(self):
        pizzas = {0: [0, 1, 2],
                  1: [3, 4, 5],
                  2: [6, 3, 1],
                  3: [4, 3, 5],
                  4: [6, 5]}
        expected_pizzeria = Pizzeria(pizzas, 7)
        expected_competition = Competition(1, 2, 1)
        result_pizzeria, result_competition = read_file(f'{test_files_path}/../doc/a_example')

        assert result_competition == expected_competition
        assert result_pizzeria == expected_pizzeria
