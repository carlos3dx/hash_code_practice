import pytest

from components.score_calculator import ScoreCalculator


class TestScoreCalculator():
    @pytest.fixture
    def calculator(self):
        pizzas = {0: [0, 1, 2],
                  1: [3, 4, 5],
                  2: [6, 3, 1],
                  3: [4, 3, 5],
                  4: [6, 5]}
        calculator = ScoreCalculator(pizzas)
        yield calculator

    def test_calculate_scores(self, calculator):
        solution_a = [[2, 1, 4], [3, 0, 2, 3]]
        solution_b = []
        solution_c = [[2, 1, 4]]
        solution_d = [[4, 0, 1, 2, 4]]
        solution_e = [[3, 4, 3, 2], [2, 1, 0]]
        solution_f = [[3, 0, 2, 3]]

        assert calculator.calculate(solution_a) == 65
        assert calculator.calculate(solution_b) == 0
        assert calculator.calculate(solution_c) == 16
        assert calculator.calculate(solution_d) == 49
        assert calculator.calculate(solution_e) == 61
        assert calculator.calculate(solution_f) == 49

