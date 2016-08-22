# coding=utf-8


class Team:
    def _init__(self, id, wiimote, team_name):
        self.id = id
        self.team_name = team_name
        self.wiimote = wiimote
        self.points = 0
        self.is_buzzing = False

    def add_points(self, val):
        self.points += val
