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

        breeder = Breeder(pizzas, validator, competition, 0)

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

        breeder = Breeder(pizzas, validator, competition, 0)

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

        breeder = Breeder(pizzas, validator, competition, 0)

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

        breeder = Breeder(pizzas, validator, competition, 0)

        result = breeder.breed(parent_a, parent_b)

        assert len(result) == 4
        for expected_child in expected_childs:
            assert expected_child in result

    def test_mutate_with_available_pizzas(self):
        num_pizzas = 5
        pizzas = list(range(num_pizzas))
        input_result = [[2, 0, 1], [2, 2, 3]]

        possible_valid_outcomes = [
            [[2, 0, 1], [2, 2, 4]],
            [[2, 0, 1], [2, 4, 3]],
            [[2, 0, 4], [2, 2, 3]],
            [[2, 4, 1], [2, 2, 3]]
        ]

        competition = Competition(2, 0, 0)
        validator = Validator(competition, num_pizzas)

        breeder = Breeder(pizzas, validator, competition, 100)

        result = breeder.mutate(input_result)

        assert result in possible_valid_outcomes

    def test_given_known_bad_result_verify_and_correct_provides_a_good_one(self):
        num_pizzas = 500
        pizzas = list(range(num_pizzas))
        input_result = [[3, 331, 64, 242], [4, 25, 243, 282, 273], [4, 345, 354, 89, 133], [2, 196, 337], [2, 126, 393],
         [3, 434, 329, 312], [3, 438, 255, 37], [2, 73, 94], [4, 395, 212, 357, 85], [4, 103, 347, 361, 420],
         [4, 46, 370, 408, 355], [2, 189, 402], [2, 167, 58], [3, 81, 314, 66], [3, 324, 235, 261], [2, 252, 16],
         [2, 399, 88], [3, 61, 462, 13], [2, 175, 22], [4, 123, 120, 436, 165], [4, 360, 43, 422, 161], [2, 367, 431],
         [2, 225, 233], [2, 263, 130], [3, 127, 149, 118], [4, 409, 452, 50, 100], [3, 290, 96, 250],
         [4, 332, 170, 102, 144], [4, 77, 135, 351, 137], [2, 311, 7], [3, 84, 456, 450], [2, 202, 376],
         [3, 447, 268, 403], [4, 405, 39, 365, 113], [2, 407, 483], [2, 97, 90], [2, 117, 156], [3, 205, 301, 340],
         [4, 141, 432, 421, 369], [4, 406, 496, 441, 396], [4, 188, 234, 29, 230], [2, 33, 326], [3, 249, 371, 404],
         [4, 315, 353, 426, 287], [4, 169, 166, 76, 448], [4, 59, 251, 208, 323], [4, 180, 139, 339, 286],
         [4, 163, 498, 150, 424], [4, 283, 152, 442, 327], [3, 391, 151, 368], [4, 423, 313, 98, 44], [2, 278, 143],
         [2, 3, 213], [3, 494, 382, 453], [2, 404, 457], [2, 193, 462], [2, 472, 127], [2, 104, 51], [3, 380, 270, 409],
         [2, 103, 42], [4, 345, 172, 227, 442], [2, 78, 312], [3, 14, 297, 436], [3, 182, 354, 333],
         [4, 107, 491, 215, 108], [3, 339, 275, 490], [4, 257, 175, 485, 13], [2, 340, 72], [4, 40, 493, 1, 434],
         [2, 349, 263], [3, 328, 402, 220], [3, 320, 212, 408], [3, 374, 145, 285], [4, 62, 266, 386, 9], [2, 425, 458],
         [4, 232, 357, 303, 396], [2, 443, 336], [3, 298, 166, 300], [4, 23, 76, 278, 383], [4, 153, 32, 289, 310],
         [2, 317, 405], [4, 35, 149, 70, 96], [4, 65, 331, 356, 467], [4, 15, 159, 377, 198], [2, 146, 311],
         [3, 114, 423, 55], [2, 483, 307], [2, 50, 188], [4, 242, 410, 0, 169], [4, 375, 264, 6, 134],
         [3, 391, 238, 20], [4, 91, 144, 422, 269], [2, 355, 248], [2, 481, 252], [3, 97, 137, 118],
         [4, 283, 344, 478, 93], [4, 459, 187, 274, 499], [4, 31, 260, 183, 7], [2, 109, 316], [3, 203, 113, 75],
         [2, 370, 30], [3, 217, 26, 262], [2, 497, 219], [2, 446, 305], [3, 230, 60, 225], [3, 47, 58, 315],
         [4, 382, 351, 272, 214], [4, 205, 251, 455, 90], [2, 403, 111], [3, 49, 250, 265], [2, 138, 412],
         [2, 430, 341], [4, 46, 57, 191, 249], [4, 179, 447, 395, 329], [2, 268, 115], [2, 80, 489],
         [4, 477, 99, 253, 234], [4, 475, 34, 206, 463], [3, 125, 63, 98], [2, 417, 202], [4, 296, 11, 148, 323],
         [4, 281, 261, 163, 243], [2, 168, 84], [4, 470, 22, 29, 156], [3, 200, 379, 439], [2, 19, 392],
         [4, 284, 381, 54, 406], [4, 52, 433, 167, 338], [2, 66, 304], [3, 494, 276, 176], [2, 165, 366],
         [3, 407, 44, 259], [4, 369, 254, 3, 286], [4, 143, 368, 197, 209], [2, 437, 233], [3, 129, 290, 279],
         [4, 213, 74, 498, 309], [3, 117, 372, 207], [2, 452, 461], [2, 385, 150], [3, 362, 92, 8], [2, 152, 347],
         [4, 43, 384, 387, 469], [4, 401, 449, 473, 236], [4, 273, 390, 81, 210], [2, 480, 25], [4, 465, 448, 394, 432],
         [3, 218, 221, 495], [3, 431, 5, 364], [3, 293, 361, 294], [4, 415, 352, 420, 178], [4, 128, 318, 271, 24],
         [2, 73, 112], [2, 184, 123], [3, 440, 326, 350], [4, 325, 343, 301, 267], [4, 208, 132, 195, 229],
         [3, 241, 466, 216], [3, 314, 464, 426], [3, 106, 171, 85], [3, 67, 419, 174], [4, 288, 199, 239, 164],
         [2, 476, 414], [4, 237, 474, 438, 486], [3, 363, 151, 157], [3, 185, 397, 64], [3, 445, 133, 139],
         [3, 131, 2, 228], [3, 95, 223, 94], [2, 196, 456]]

        competition = Competition(65, 60, 60)
        validator = Validator(competition, num_pizzas)

        breeder = Breeder(pizzas, validator, competition, 0)

        result = breeder.verify_and_correct(input_result)
        assert validator.validate(result)

    def test_mutate_without_available_pizzas(self):
        num_pizzas = 4
        pizzas = list(range(num_pizzas))
        input_result = [[2, 0, 1], [2, 2, 3]]

        possible_valid_outcomes = [
            [[2, 0, 3], [2, 2, 1]],
            [[2, 0, 2], [2, 1, 3]],
            [[2, 3, 1], [2, 2, 0]],
            [[2, 2, 1], [2, 0, 3]]
        ]

        competition = Competition(2, 0, 0)
        validator = Validator(competition, num_pizzas)

        breeder = Breeder(pizzas, validator, competition, 100)

        result = breeder.mutate(input_result)

        assert result in possible_valid_outcomes
