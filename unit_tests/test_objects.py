from components.competition import Competition
from components.pizzeria import Pizzeria


class TestObjects:
    def test_two_identical_pizzeria_objects(self):
        p1 = Pizzeria({'p1': [1, 2, 3], 'p2': [4, 5, 6]}, 6)
        p2 = Pizzeria({'p1': [1, 2, 3], 'p2': [4, 5, 6]}, 6)
        assert p1 == p2

    def test_two_different_pizzeria_objects(self):
        p1 = Pizzeria({'p1': [1, 2, 3], 'p2': [4, 5, 6]}, 6)
        p2 = Pizzeria({'p1': [1, 2, 3, 0], 'p2': [4, 5, 6]}, 7)
        assert p1 != p2

    def test_pizzeria_against_other_object(self):
        p1 = Pizzeria({'p1': [1, 2, 3], 'p2': [4, 5, 6]}, 6)
        p2 = 'mock'
        assert p1 != p2

    def test_two_identical_competition_objects(self):
        c1 = Competition(3, 4, 5)
        c2 = Competition(3, 4, 5)
        assert c1 == c2

    def test_two_different_competition_objects(self):
        c1 = Competition(5, 4, 3)
        c2 = Competition(3, 4, 5)
        assert c1 != c2

    def test_competition_against_other_object(self):
        c1 = Competition(5, 4, 3)
        c2 = 'mock'
        assert c1 != c2
