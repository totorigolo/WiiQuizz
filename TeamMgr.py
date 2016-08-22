# coding=utf-8

from Singleton import Singleton
from Team import Team
from constants import *


@Singleton
class TeamMgr:
    """
        Team Manager
        Attention, une fenêtre doit être active pour utiliser les méthodes
    """
    def __init__(self, nb_players, max_simult_buzzer=1):
        """
        Nombre de personne pouvant buzzer simultanément (si -1, pas de restrictions)
        :param nb_players: nombre de joueurs en jeu
        :param max_simult_buzzer: nombre de personne pouvant buzzer simultanément
        """
        self.players = {}
        self.max_simult_buzzer = max_simult_buzzer
        self.wining_points = WINING_POINTS
        self.losing_points = LOSING_POINTS
        self.buzzing = []
        self.nb_players = nb_players

    def add_player(self, name, wiimote, team_name):
        """
        Ajoute un joueur
        :param name: nom du joueur noms : team1, team2, team3, team4
        :param wiimote: wiimote du joueur
        :param team_name: Nom de l'équipe apparente (Pastèque, Ananas, ...)
        """
        self.players[name] = Team(name, wiimote, team_name)

    def buzz(self, name):
        """
        Fait buzzer une équipe
        :param name: nom de l'équipe qui buzz
        :return: bool
        """
        if self.max_simult_buzzer != -1 and len(self.buzzing) >= self.max_simult_buzzer:
            return False
        self.buzzing.append(name)
        self.players[name].is_buzzing = True
        self.players[name].wiimote.vibrer()
        return True

    def accept_buzz(self, name, points=None):
        """
        Accepter un buzz
        :param name: nom de l'équipe
        :param points: nombre de point à ajouter
        :return: nombre de points ajoutés None si pas de point ajoutés
        """
        if points is None:
            points = self.wining_points
        try:
            self.buzzing.remove(name)
        except ValueError:
            return
        else:
            self.players[name].is_buzzing = False
            self.players[name].add_points(points)
        return points

    def refuse_buzz(self, name, points=None):
        """
        Refuser un buzz
        :param name: nom de l'équipe
        :param points: nombre de points à enlever (facultatif)
        :return: le nombre de points enlevé None si pas de points enlevé
        """
        if points is None:
            points = self.losing_points
        try:
            self.buzzing.remove(name)
        except ValueError:
            return
        else:
            self.players[name].is_buzzing = False
            self.players[name].add_points(-points)
        return -points

    def cancel_buzz(self, name):
        """
        Annule un buzz
        :param name: nom de l'équipe à annuler
        """
        try:
            self.buzzing.remove(name)
        except ValueError:
            return
        else:
            self.players[name].is_buzzing = False

    def add_points(self, name, points):
        """
        Ajoute des points à une équipe
        :param name: nom de l'équipe
        :param points: nombre de points
        """
        self.players[name].add_points(points)

    def get_best_player(self):
        max_points = 0
        best_players = []
        for name, p in self.players.items():
            if p.points == max_points:
                best_players.append(name)
            elif p.points > max_points:
                best_players = []
                max_points = p.points
        return best_players
