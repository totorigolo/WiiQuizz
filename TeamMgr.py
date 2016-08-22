# coding=utf-8

from Singleton import Singleton
from Team import Team
from WindowHelper import WindowHelper


@Singleton
class TeamMgr:
    """
    Cette classe s'occupe de la gestion des équipes. C'est elle qui gère :
     - les scores
     - les pénalités ou bonus
     - les noms des équipes et leur couleur
     - l'affichage des scores
     - la joie à la victoire, et la déception à la défaite
    """

    # TODO: Lesquelles ? ("ATTENTION : une fenêtre doit être active pour utiliser les méthodes.")

    def __init__(self, max_simult_buzzer=1):
        """
        :param max_simult_buzzer: nombre de personne pouvant buzzer simultanément (si -1, pas de restrictions)
        """
        self.teams = {}
        self.max_simult_buzzer = max_simult_buzzer
        self.buzzing_teams = []
        self.wining_points = 0
        self.losing_points = 0
        self.set_score_mode()

        self.win = WindowHelper.Instance()

        self.win.new_color((255, 0, 96), 'team1')
        self.win.new_color((252, 255, 0), 'team2')
        self.win.new_color((58, 119, 71), 'team3')
        self.win.new_color((255, 162, 0), 'team4')

        self.win.new_font('Arial', 40, 'title')
        self.win.new_font('Arial', 70, 'very_big')

        # Couleur des textes
        self.color_correspondence = {
            'team1': 'team2',
            'team2': 'team1',
            'team3': 'team4',
            'team4': 'team4'
        }

    def draw_scores(self, page_label):
        """
        Affiche les scores sur la page
        :param page_label: label de la page sur lequel afficher les scores
        """
        self.win.go_to(page_label)
        name_template = '{}_players'.format(len(self.teams))
        for id, team in self.teams:
            team_num = "team{}".format(id)
            self.win.new_text(team.team_name, 'very_big', self.color_correspondence[team_num], label=team_num)
            self.win.new_text(str(team.points), 'title', self.color_correspondence[team_num], label=(team_num+'_result'))
        self.win.import_template(name_template)

        self.win.refresh()


    def add_team(self, id, wiimote, team_name):
        """
        Ajoute un joueur.
        :param id: nom du joueur noms : 1 à 4
        :param wiimote: wiimote du joueur.
        :param team_name: Nom de l'équipe apparente (Pastèque, Ananas, ...)
        """
        # TODO: Gérer 'new'
        self.teams[id] = Team(id, wiimote, team_name)

    def set_score_mode(self, mode='add_only', wining_points=None, loosing_points=None):
        """
        Permet de définir comment sont donnés les points pour une bonne ou une mauvaise réponse. La méthode d'ajout
        varie suivant le mode de score, indiqué par how_many.
        Les modes de score disponibles sont :
          - 'add_only' : add=Ajout de 500 points, loose=Retrait de zéro point.
          - 'add_more' : add=Ajout de 500 points, loose=Retrait de 100 point.
          - 'equal' : add=Ajout de 500 points, loose=Retrait de 500 point.
          - 'hardcore' : add=Ajout de 100 points, loose=Retrait de 500 point.
          - 'perso' : utilisation des points fournis en paramètres
        Le mode par défaut est 'add_more'.
        :param mode: nouveau mode à adopter
        :type wining_points: object
        :param loosing_points:
        """
        if mode == 'add_only':
            self.wining_points, self.losing_points = 500, 0
        elif mode == 'add_more':
            self.wining_points, self.losing_points = 500, 100
        elif mode == 'equal':
            self.wining_points, self.losing_points = 300, 300
        elif mode == 'hardcore':
            self.wining_points, self.losing_points = 100, 500
        elif mode == 'perso' and wining_points is not None and loosing_points is not None:
            self.wining_points, self.losing_points = wining_points, loosing_points
        else:
            print "Mode inconnu. Par défaut, mode 'add_more' utilisé."
            self.set_score_mode()

    def buzz(self, id):
        """
        Tente de faire buzzer une équipe. Si une équipe a buzzé avant nous, notre requête est ignorée et False est
        retourné. Si c'est accepté, alors True est retourné.
        :param id: id de l'équipe qui veut buzzer
        :return: boolean indiquant si ça a fonctionné
        """
        if self.max_simult_buzzer != -1 and len(self.buzzing_teams) >= self.max_simult_buzzer:
            return False
        self.buzzing_teams.append(id)
        self.teams[id].is_buzzing = True
        self.teams[id].wiimote.vibrer()
        return True

    def accept_buzz(self, id, points=None):
        """
        Accepter un buzz (ex: bonne réponse).
        :param id: id de l'équipe
        :param points: nombre de point à ajouter. Ne pas fournir points (None) revient à utiliser le score_mode en cours
        :return: nombre de points ajoutés. None si pas de point ajoutés et False si id n'a pas buzzé
        """
        if points is None:
            points = self.wining_points
        try:
            self.buzzing_teams.remove(id)
        except ValueError:
            return False
        else:
            self.teams[id].is_buzzing = False
            self.teams[id].add_points(points)
        return points

    def refuse_buzz(self, id, points=None):
        """
        Refuser un buzz (ex: mauvaise réponse)
        :param id: id de l'équipe
        :param points: nombre de point à retirer. Ne pas fournir points (None) revient à utiliser le score_mode en cours
        :return: nombre de points retirés. None si pas de point retirés et False si id n'a pas buzzé
        """
        if points is None:
            points = self.losing_points
        try:
            self.buzzing_teams.remove(id)
        except ValueError:
            return False
        else:
            self.teams[id].is_buzzing = False
            self.teams[id].add_points(-points)
        return -points

    def cancel_buzz(self, name):
        """
        Annule un buzz
        :param name: id de l'équipe à annuler
        :return: True si l'annulation a réussi, False sinon.
        """
        try:
            self.buzzing_teams.remove(name)
        except ValueError:
            return
        else:
            self.teams[name].is_buzzing = False
        return True

    def clear_buzzes(self):
        """
        Annule tous les buzzs
        """
        for t in self.buzzing_teams:
            self.teams[t].is_buzzing = False
        self.buzzing_teams = []

    def add_points(self, id, points):
        """
        Ajoute des points à une équipe. ATTENTION : utiliser accept_buzz et refuse_buzz pour gérer les buzzers et
        ajouter des points dans le même temps. Cette fonction sert, par exemple, à ajouter des bonus aux équipes.
        :param id: id de l'équipe
        :param points: nombre de points à ajouter. Fournir un nombre négatif pour en enlever.
        """
        self.teams[id].add_points(points)

    def get_best_team(self):
        """
        Permet de connaitre la ou les meilleure(s) équipe, en terme de score.
        :return: Un tableau contenant la meilleure équipe, ou les meilleurs si ex-aequo
        """
        max_points = 0
        best_players = []
        for name, p in self.teams.items():
            if p.points == max_points:
                best_players.append(name)
            elif p.points > max_points:
                best_players = []
                max_points = p.points
        return best_players
