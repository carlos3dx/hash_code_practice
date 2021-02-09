from components.breeder import Breeder
from components.competition import Competition
from components.validator import Validator


class TestBreeder:
    def test_breed_when_no_conflict_possible_and_no_mutation(self):
        num_pizzas = 8
        pizzas = list(range(num_pizzas))
        parent_a = [[2, 0, 1], [2, 2, 3]]
        parent_b = [[2, 4, 5], [2, 6, 7]]

        expected_childs = [
            [[2, 0, 1], [2, 6, 7]],
            [[2, 4, 5], [2, 2, 3]],
            [[2, 2, 3], [2, 4, 5]],
            [[2, 6, 7], [2, 0, 1]]
        ]

        competition = Competition(2, 0, 0)
        validator = Validator(competition, num_pizzas)

        breeder = Breeder(pizzas, validator, 0)

        result = breeder.breed(parent_a, parent_b)

        assert len(result) == 4
        for expected_child in expected_childs:
            assert expected_child in result

    def test_breed_when_conflict_possible_and_extra_pizzas_available(self):
        num_pizzas = 8
        pizzas = list(range(num_pizzas))
        parent_a = [[2, 6, 1], [2, 2, 3]]
        parent_b = [[2, 2, 5], [2, 6, 7]]

        expected_childs = [
            [[2, 5, 1], [2, 6, 7]],
            [[2, 7, 5], [2, 2, 3]],
            [[2, 5, 7], [2, 6, 1]],
            [[2, 7, 3], [2, 2, 5]]
        ]

        competition = Competition(2, 0, 0)
        validator = Validator(competition, num_pizzas)

        breeder = Breeder(pizzas, validator, 0)

        result = breeder.breed(parent_a, parent_b)

        assert len(result) == 4
        for expected_child in expected_childs:
            assert expected_child in result

    def test_breed_when_conflict_possible_and_no_extra_pizzas_available(self):
        num_pizzas = 5
        pizzas = list(range(num_pizzas))
        parent_a = [[2, 2, 4], [3, 0, 1, 3]]
        parent_b = [[3, 4, 1, 2], [2, 0, 3]]

        expected_childs = [
            [[2, 2, 4], [2, 0, 3]],
            [[3, 0, 1, 3]],
            [[2, 0, 3], [2, 2, 4]],
            [[3, 4, 1, 2]]
        ]

        competition = Competition(2, 2, 0)
        validator = Validator(competition, num_pizzas)

        breeder = Breeder(pizzas, validator, 0)

        result = breeder.breed(parent_a, parent_b)

        assert len(result) == 4
        for expected_child in expected_childs:
            assert expected_child in result

    def test_breed_when_conflict_inevitable_and_no_extra_pizzas_available(self):
        num_pizzas = 5
        pizzas = list(range(num_pizzas))
        parent_a = [[2, 2, 4], [3, 0, 1, 3], [3, 0, 1, 3]]
        parent_b = [[3, 4, 1, 2], [2, 0, 3], [2, 0, 3]]

        expected_childs = [
            [[2, 2, 4], [2, 0, 3]],
            [[3, 0, 1, 3]],
            [[2, 0, 3], [2, 2, 4]],
            [[3, 4, 1, 2]]
        ]

        competition = Competition(2, 2, 0)
        validator = Validator(competition, num_pizzas)

        breeder = Breeder(pizzas, validator, 0)

        result = breeder.breed(parent_a, parent_b)

        assert len(result) == 4
        for expected_child in expected_childs:
            assert expected_child in result
