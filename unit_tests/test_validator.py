import pytest

from components.competition import Competition
from components.validator import Validator


class TestValidator():
    @pytest.fixture
    def validator(self):
        num_pizzas = 30
        competition = Competition(1, 2, 1)
        validator = Validator(competition, num_pizzas)
        yield validator

    def test_valid_solutions(self, validator):
        solution_a = [[2, 1, 4], [3, 0, 2, 3]]
        solution_b = []
        solution_c = [[2, 1, 4]]
        solution_d = [[4, 0, 1, 2, 4]]
        solution_e = [[3, 4, 3, 2], [2, 1, 0]]

        assert validator.validate(solution_a)
        assert validator.validate(solution_b)
        assert validator.validate(solution_c)
        assert validator.validate(solution_d)
        assert validator.validate(solution_e)

    def test_invalid_solutions(self, validator):
        solution_a = [[2, 1], [3, 0, 2, 3]]  # less pizzas than people
        solution_b = [[2, 0, 1], [3, 2, 3, 4], [3, 5, 6, 7], [4, 8, 9, 10, 11],
                      [2, 12, 13]]  # more deliveries than teams
        solution_c = [[]]  # invalid format
        solution_d = [[2, 10, 500]]  # invalid pizza id
        solution_e = [[2, 1, 2], [2, 0, 1]]  # duplicated pizza id across two teams
        solution_f = [[2, 1, 1], [2, 0, 2]]  # duplicated pizza id in same team

        assert not validator.validate(solution_a)
        assert not validator.validate(solution_b)
        assert not validator.validate(solution_c)
        assert not validator.validate(solution_d)
        assert not validator.validate(solution_e)
        assert not validator.validate(solution_f)

    def test_invalid_solution_with_different_competition(self):
        num_pizzas = 5
        competition = Competition(2, 2, 0)
        validator = Validator(competition, num_pizzas)

        solution_a = [[2, 2, 4], [2, 1, 3], [2, 0, 3]]

        assert not validator.validate(solution_a)