class Competition:
    def __init__(self, teams_of_two: int, teams_of_three: int, teams_of_four: int) -> None:
        self.teams_of_two = teams_of_two
        self.teams_of_three = teams_of_three
        self.teams_of_four = teams_of_four
        self.total_teams = teams_of_two + teams_of_three + teams_of_four
        self.total_people = teams_of_two * 2 + teams_of_three * 3 + teams_of_four * 4

    def __eq__(self, other):
        return isinstance(other, Competition) and \
            self.teams_of_two == other.teams_of_two and \
            self.teams_of_three == other.teams_of_three and \
            self.teams_of_four == other.teams_of_four
