# coding=utf-8


class Team:
    def __init__(self, id, buzzer, team_name):
        self.id = id
        self.team_name = team_name
        self.buzzer = buzzer
        self.points = 0
        self.is_buzzing = False

    def add_points(self, val):
        self.points += val
